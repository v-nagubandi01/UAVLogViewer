from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Any
import os
import shutil
import uuid
import time
from parser import bin_to_dataframe_optimized
from deepagent import create_graph
import tempfile
import shutil
from langchain_core.messages import ToolMessage
import pandas as pd


app = FastAPI(title="UAV Log Viewer Backend", version="1.0.0")

# Add CORS middleware with more restrictive settings
# In production, replace with specific frontend URLs
allowed_origins = [
    "http://localhost:3000",  # React development server
    "http://localhost:3001",  # Alternative React port
    "http://127.0.0.1:3000",  # Localhost alternative
    "http://127.0.0.1:3001",  # Localhost alternative
    # Add your production frontend URL here
    # "https://your-frontend-domain.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Specific methods only
    allow_headers=["Content-Type", "Authorization", "Accept"],  # Specific headers only
)


class ChatMessage(BaseModel):
    message: str
    conversationId: str


class ChatResponse(BaseModel):
    response: str


class UploadDataRequest(BaseModel):
    conversation_id: str


class UploadDataResponse(BaseModel):
    status: str
    message: str = ""
    conversation_id: str = ""


class SessionInfo(BaseModel):
    session_id: str
    filename: str = ""
    message_count: int = 0
    number_of_user_questions: int = 0
    created_at: str = ""


class SessionInfoResponse(BaseModel):
    total_sessions: int
    active_sessions: List[SessionInfo]


class MessagesUploadRequest(BaseModel):
    conversationId: str
    messages: Dict[str, Any]


class MessagesUploadResponse(BaseModel):
    status: str
    message: str = ""


sessions = {}
# Track session metadata for better management
session_metadata = {}


def convert_messages_to_dataframes(messages: Dict[str, Any]) -> Dict[str, pd.DataFrame]:
    """
    Convert frontend messages to pandas DataFrames.
    Each message type (including XKQ[0], XKQ[1], etc.) is treated as a separate DataFrame.
    
    Args:
        messages: Dictionary of message types with their data arrays
        
    Returns:
        Dictionary of DataFrames keyed by message name
    """

    result_dfs = {}
    
    for msg_type, msg_data in messages.items():

        if msg_type == "EV":
            print (msg_data)
        # Skip if not a dictionary or empty
        if not isinstance(msg_data, dict) or not msg_data:
            continue
        
        # Create DataFrame from the message data
        try:
            df = pd.DataFrame(msg_data)
            result_dfs[msg_type] = df
        except Exception as e:
            print(f"Warning: Could not convert {msg_type} to DataFrame: {e}")
            continue
    
    return result_dfs

@app.get("/")
async def root():
    return {"message": "UAV Log Viewer Backend is running"}


@app.get("/session-info", response_model=SessionInfoResponse)
async def get_session_info():
    """
    Get information about active sessions including count and details.
    """
    global sessions, session_metadata
    
    active_sessions = []
    
    for session_id in sessions.keys():
        session_data = sessions[session_id]
        metadata = session_metadata.get(session_id, {})
        
        session_info = SessionInfo(
            session_id=session_id,
            filename=metadata.get("filename", "Unknown"),
            message_count=len(session_data.get("messages", [])),
            number_of_user_questions=metadata.get("number_of_user_questions", 0),
            created_at=metadata.get("created_at", "Unknown")
        )
        active_sessions.append(session_info)
    
    return SessionInfoResponse(
        total_sessions=len(sessions),
        active_sessions=active_sessions
    )


@app.post("/chat", response_model=ChatResponse)
async def chat(message_data: ChatMessage) -> Dict[str, str]:
    """
    Chat endpoint that processes messages with conversation context.
    """
    global sessions
    print("\n\n\n\n")
    print(f"Received chat message for conversationId: {message_data.conversationId}")
    print(f"Message: {message_data.message}")
    print(type(message_data.conversationId))

    print("current sessions keys:")
    print(sessions.keys())

    if message_data.conversationId not in sessions:
        return {
            "response": "Error: Conversation ID not found. Please upload data first."
        }

    agent = await create_graph()

    # Measure time for agent.invoke
    start_time = time.time()

    state = sessions[message_data.conversationId]

    state["messages"] = state["messages"] + [
        {"role": "user", "content": message_data.message}
    ]
    
    # Increment user questions counter in session metadata
    if message_data.conversationId in session_metadata:
        session_metadata[message_data.conversationId]["number_of_user_questions"] += 1

    print("State messages before invoke:")
    print(state['messages'])

    result = agent.invoke(state)
    duration = time.time() - start_time
    print(f"agent.invoke took {duration:.3f} seconds")

    response_text = result['messages'][-1].content

    print("\n"*3)

    print(result.keys())


    for msg in result["messages"]:
        print(msg.content)
        print("==================================\n"*3)


    sessions[message_data.conversationId] = result

    return {"response": response_text}



@app.post("/upload-messages", response_model=MessagesUploadResponse)
async def upload_messages(request: MessagesUploadRequest) -> Dict[str, str]:
    """
    Endpoint to receive parsed messages from the frontend.
    Called once after all messages have been processed.
    """
    global sessions, session_metadata
    
    print(f"\n{'='*60}")
    print("Received /upload-messages request")
    print(f"Conversation ID: {request.conversationId}")
    print(f"{'='*60}\n")
    
    try:
        # Create session if it doesn't exist
        if request.conversationId not in sessions:
            print(f"Session not found, creating new session for {request.conversationId}")
            sessions[request.conversationId] = {
                "result_df": None,
                "message_dfs": {},
                "messages": [],  # Empty list for chat messages
            }
            session_metadata[request.conversationId] = {
                "filename": "unknown",
                "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "number_of_user_questions": 0
            }
        
        # Get message types and counts
        message_types = list(request.messages.keys())
        total_message_types = len(message_types)
        
        print(f"Received {total_message_types} message types:")
        for msg_type in message_types:
            msg_data = request.messages[msg_type]
            if isinstance(msg_data, dict) and 'time_boot_ms' in msg_data:
                count = len(msg_data['time_boot_ms'])
                print(f"  - {msg_type}: {count} entries")
            else:
                print(f"  - {msg_type}: (structure varies)")
        
        print("\nConverting messages to DataFrames...")
        # Convert messages to DataFrames
        message_dfs = convert_messages_to_dataframes(request.messages)
        
        print(f"Created {len(message_dfs)} DataFrames:")
        for msg_name, df in message_dfs.items():
            print(f"  - {msg_name}: {len(df)} rows, {len(df.columns)} columns")
        
        # Store the DataFrames in the session
        if request.conversationId in sessions:
            # Replace message_dfs with frontend parsed data
            sessions[request.conversationId]["message_dfs"] = message_dfs
            
            # Also keep raw messages if needed
            sessions[request.conversationId]["frontend_messages"] = request.messages
            
            # Update session metadata
            if request.conversationId in session_metadata:
                session_metadata[request.conversationId]["frontend_messages_received"] = True
                session_metadata[request.conversationId]["message_types_count"] = len(message_dfs)
                session_metadata[request.conversationId]["message_types"] = list(message_dfs.keys())
        
        print(f"\nSuccessfully stored DataFrames for conversation {request.conversationId}")
        print(f"{'='*60}\n")
        
        return {
            "status": "success",
            "message": f"Successfully received and converted {len(message_dfs)} message types to DataFrames"
        }
        
    except Exception as e:
        print(f"Exception occurred while processing messages: {e}")
        import traceback
        traceback.print_exc()
        return {
            "status": "error",
            "message": f"Failed to process messages: {str(e)}"
        }

