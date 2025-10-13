from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Dict, List
import os
import shutil
import uuid
import time
import asyncio
import json
from parser import bin_to_dataframe_optimized
from deepagent import create_graph
import tempfile
import shutil
from langchain_core.messages import ToolMessage


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


sessions = {}
# Track session metadata for better management
session_metadata = {}
# Track active SSE connections
active_connections = {}

@app.get("/")
async def root():
    return {"message": "UAV Log Viewer Backend is running"}


def sse_message(event: str, data: dict) -> str:
    """
    Format a message as Server-Sent Event
    """
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"


async def event_generator(conversation_id: str, message: str):
    """
    Generate SSE events by processing the agent and streaming results
    """
    global sessions, session_metadata
    
    print(f"Starting SSE stream for conversation_id: {conversation_id}")
    
    try:
        if conversation_id not in sessions:
            yield sse_message("error", {"content": "Error: Conversation ID not found. Please upload data first."})
            return
        
        # Create the agent
        agent = await create_graph()
        
        # Measure time for agent processing
        start_time = time.time()
        
        state = sessions[conversation_id]
        
        state["messages"] = state["messages"] + [
            {"role": "user", "content": message}
        ]
        
        # Increment user questions counter in session metadata
        if conversation_id in session_metadata:
            session_metadata[conversation_id]["number_of_user_questions"] += 1
        
        print("State messages before invoke:")
        print(state['messages'])
        
        # Send processing event
        yield sse_message("processing", {"content": "Processing your request..."})
        
        # Process the agent (check if it supports streaming)
        # If your agent supports astream, use it for better streaming
        # For now, we'll use invoke and send the complete response
        result = agent.invoke(state)
        
        duration = time.time() - start_time
        print(f"agent.invoke took {duration:.3f} seconds")
        
        response_text = result['messages'][-1].content
        
        print("\n"*3)
        print(result.keys())
        
        for msg in result["messages"]:
            print(msg.content)
            print("==================================\n"*3)
        
        # Update sessions with result
        sessions[conversation_id] = result
        
        # Send the response as a chunk
        yield sse_message("message", {"content": response_text})
        
        # Send completion event
        yield sse_message("complete", {"content": "Processing completed"})
        
    except asyncio.CancelledError:
        print(f"SSE stream cancelled for conversation_id: {conversation_id}")
        yield sse_message("cancelled", {"content": "Stream cancelled"})
    
    except Exception as e:
        print(f"SSE stream error for conversation_id {conversation_id}: {e}")
        yield sse_message("error", {"content": str(e)})
    
    finally:
        # Clean up connection tracking
        active_connections.pop(conversation_id, None)
        print(f"SSE stream ended for conversation_id: {conversation_id}")


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


@app.post("/chat")
async def chat_sse(message_data: ChatMessage):
    """
    Chat endpoint that streams responses using Server-Sent Events (SSE).
    """
    global active_connections
    
    print("\n\n\n\n")
    print(f"Received chat message for conversationId: {message_data.conversationId}")
    print(f"Message: {message_data.message}")
    print(type(message_data.conversationId))
    
    print("current sessions keys:")
    print(sessions.keys())
    
    # Track active connection
    active_connections[message_data.conversationId] = True
    
    # Return SSE stream with proper headers
    headers = {
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Cache-Control",
        "X-Accel-Buffering": "no",  # Disable nginx buffering
    }
    
    return StreamingResponse(
        event_generator(message_data.conversationId, message_data.message),
        media_type="text/event-stream",
        headers=headers,
    )


@app.post("/upload-data")
async def upload_data(
    file: UploadFile = File(...), conversation_id: str = Form(...)
) -> Dict[str, str]:
    global sessions
    print("Received /upload-data request")
    print(f"Conversation ID: {conversation_id}")
    print(f"Uploaded file: {file.filename}, content_type: {file.content_type}")

    try:
        # Check if the uploaded file is a .bin file
        if not file.filename.endswith('.bin'):
            print("File is not a .bin file")
            return {"status": "error", "message": "Only .bin files are allowed"}

        # Extract filename without extension
        filename_without_ext = os.path.splitext(file.filename)[0]
        temp_filename = f"{filename_without_ext}_{conversation_id}.bin"

        # Read the uploaded file into memory
        file_contents = await file.read()  # async read

        # Create a temporary file that provides a real file path
        with tempfile.NamedTemporaryFile(delete=False, suffix=".bin") as tmp_file:
            tmp_file.write(file_contents)
            tmp_file_path = tmp_file.name

        message_dfs = bin_to_dataframe_optimized(tmp_file_path)

        sessions[str(conversation_id)] = {
            "result_df": None,
            "message_dfs": message_dfs,
            "messages": [],
        }
        
        # Store session metadata
        session_metadata[str(conversation_id)] = {
            "filename": file.filename,
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "number_of_user_questions": 0
        }

        print(f"File ready in temp path: {tmp_file_path}")
        print(sessions.keys())

        return {"status": "success", "message": f"File processed as {temp_filename}"}

    except Exception as e:
        print(f"Exception occurred: {e}")
        return {"status": "error", "message": f"Failed to process file: {str(e)}"}

