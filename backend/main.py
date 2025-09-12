from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict

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
async def upload_data(data: UploadDataRequest) -> Dict[str, str]:
    """
    Upload data endpoint that accepts conversation_id and returns success status.
    """
    return {"status": "ok"}
