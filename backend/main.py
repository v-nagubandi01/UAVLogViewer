from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict
import os
import shutil
import uuid
import time

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

@app.get("/")
async def root():
    return {"message": "UAV Log Viewer Backend is running"}

@app.post("/chat", response_model=ChatResponse)
async def chat(message_data: ChatMessage) -> Dict[str, str]:
    """
    Chat endpoint that processes messages with conversation context.
    """
    print(f"Received chat message for conversationId: {message_data.conversationId}")
    print(f"Message: {message_data.message}")

    # Simulate processing time (remove this in production)
    time.sleep(2)
    
    # TODO: Implement actual chat logic with conversation context
    # For now, return a response that demonstrates markdown support
    response_text = f"""## Chat Response

**Conversation ID:** `{message_data.conversationId}`

**Your message:** {message_data.message}

### Features Available:
- ✅ **Markdown formatting** (bold, italic, headers, lists)
- ✅ **Code blocks** with syntax highlighting
- ✅ **Loading indicators** during processing
- ✅ **Error handling** with detailed messages

### Example Code Block:
```python
def process_message(msg, conv_id):
    return f"Processed: {{msg}} for {{conv_id}}"
```

*This is a demo response showing markdown capabilities.*"""
    
    return {"response": response_text}

@app.post("/upload-data", response_model=UploadDataResponse)
async def upload_data(
    file: UploadFile = File(...),
    conversation_id: str = Form(default=None)
) -> Dict[str, str]:
    """
    Upload data endpoint that accepts file uploads and conversation_id.
    Saves uploaded .bin file into conversation_data/ with name <filename>_<conversation_id>.bin
    If no conversation_id is provided, generates a UUID.
    """
    print("Received /upload-data request")
    
    # Generate UUID if no conversation_id provided
    if conversation_id is None:
        conversation_id = str(uuid.uuid4())
        print(f"Generated new conversation_id: {conversation_id}")
    else:
        print(f"Using provided conversation_id: {conversation_id}")
    
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

        res = {"status": "success", "message": f"File saved as {new_filename}", "conversation_id": conversation_id}
        return res

    except Exception as e:
        print(f"Exception occurred: {e}")
        return {"status": "error", "message": f"Failed to save file: {str(e)}"}


