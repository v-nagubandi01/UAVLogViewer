from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict
import os
import shutil

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

class ChatResponse(BaseModel):
    response: str

class UploadDataRequest(BaseModel):
    conversation_id: str

class UploadDataResponse(BaseModel):
    status: str
    message: str = ""

@app.get("/")
async def root():
    return {"message": "UAV Log Viewer Backend is running"}

@app.post("/chat", response_model=ChatResponse)
async def chat(message_data: ChatMessage) -> Dict[str, str]:
    """
    Chat endpoint that echoes back the received message.
    """
    return {"response": f"You said: {message_data.message}"}

@app.post("/upload-data", response_model=UploadDataResponse)
async def upload_data(
    file: UploadFile = File(...),
    conversation_id: str = Form(...)
) -> Dict[str, str]:
    """
    Upload data endpoint that accepts file uploads and conversation_id.
    Saves uploaded .bin file into conversation_data/ with name <filename>_<conversation_id>.bin
    """
    print("Received /upload-data request")
    print(f"Conversation ID: {conversation_id}")
    print(f"Uploaded file: {file.filename}, content_type: {file.content_type}")

    try:
        # Create conversation_data directory if it doesn't exist
        conversation_data_dir = "conversation_data"
        os.makedirs(conversation_data_dir, exist_ok=True)
        print(f"Ensured conversation_data directory exists at: {conversation_data_dir}")

        # Check if the uploaded file is a .bin file
        if not file.filename.endswith('.bin'):
            print("File is not a .bin file")
            return {"status": "error", "message": "Only .bin files are allowed"}

        # Extract filename without extension
        filename_without_ext = os.path.splitext(file.filename)[0]
        print(f"Filename without extension: {filename_without_ext}")

        # Create the new filename: <filename>_<conversation_id>.bin
        new_filename = f"{filename_without_ext}_{conversation_id}.bin"
        file_path = os.path.join(conversation_data_dir, new_filename)
        print(f"Saving file as: {file_path}")

        # Save the uploaded file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        print(f"File saved successfully: {new_filename}")
        return {"status": "success", "message": f"File saved as {new_filename}"}

    except Exception as e:
        print(f"Exception occurred: {e}")
        return {"status": "error", "message": f"Failed to save file: {str(e)}"}


