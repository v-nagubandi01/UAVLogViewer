from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict

app = FastAPI(title="UAV Log Viewer Backend", version="1.0.0")

class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@app.get("/")
async def root():
    return {"message": "UAV Log Viewer Backend is running"}

@app.post("/chat", response_model=ChatResponse)
async def chat(message_data: ChatMessage) -> Dict[str, str]:
    """
    Chat endpoint that echoes back the received message.
    """
    return {"response": f"You said: {message_data.message}"}
