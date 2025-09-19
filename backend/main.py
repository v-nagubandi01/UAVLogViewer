from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict
import os
import shutil
import uuid
import time
from parser import bin_to_dataframe_optimized
from deepagent import create_graph
import tempfile
import shutil
from langchain_core.messages import ToolMessage


app = FastAPI(title="UAV Log Viewer Backend", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
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


sessions = {}

@app.get("/")
async def root():
    return {"message": "UAV Log Viewer Backend is running"}


@app.post("/chat", response_model=ChatResponse)
async def chat(message_data: ChatMessage) -> Dict[str, str]:
    """
    Chat endpoint that processes messages with conversation context.
    """
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

    print("State messages before invoke:")
    print(state['messages'])

    result = agent.invoke(state)
    duration = time.time() - start_time
    print(f"agent.invoke took {duration:.3f} seconds")

    response_text = result['messages'][-1].content

    #To Do items are uncessary use of context which doesn't need to be stored.
    filtered_messages = []

    for msg in result['messages']:
        if isinstance(msg, ToolMessage):
            if msg.name == "write_todos":
                continue
        filtered_messages.append(msg)
    
    state["messages"] = filtered_messages

    return {"response": response_text}


@app.post("/upload-data")
async def upload_data(
    file: UploadFile = File(...), conversation_id: str = Form(...)
) -> Dict[str, str]:
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

        start_time = time.time()
        message_dfs = bin_to_dataframe_optimized(tmp_file_path)
        duration = time.time() - start_time
        print(f"bin_to_dataframe_optimized took {duration:.3f} seconds")

        global sessions
        sessions[str(conversation_id)] = {
            "result_df": None,
            "message_dfs": message_dfs,
            "messages": [],
        }

        print(f"File ready in temp path: {tmp_file_path}")
        print(sessions.keys())

        return {"status": "success", "message": f"File processed as {temp_filename}"}

    except Exception as e:
        print(f"Exception occurred: {e}")
        return {"status": "error", "message": f"Failed to process file: {str(e)}"}
