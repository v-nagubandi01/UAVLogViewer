# UAV Log Viewer Backend

A FastAPI backend for the UAV Log Viewer application.

## Setup

1. Create and activate a virtual environment:
```bash
python3.11 -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Server

Start the development server:
```bash
uvicorn main:app --reload --port 8001
```

The server will be available at `http://localhost:8001`

## API Endpoints

### GET /
Returns a simple status message.

**Response:**
```json
{
  "message": "UAV Log Viewer Backend is running"
}
```

### POST /chat
Accepts a chat message and echoes it back.

**Request Body:**
```json
{
  "message": "Your message here"
}
```

**Response:**
```json
{
  "response": "You said: Your message here"
}
```

### POST /upload-data
Accepts a `.bin` file upload and a `conversation_id`. Saves the file as `<filename>_<conversation_id>.bin` in the `conversation_data/` directory.

**Form Data:**
- `file`: The `.bin` file to upload (required)
- `conversation_id`: The conversation ID (required)

**Response (success):**
```json
{
  "status": "success",
  "message": "File saved as <filename>_<conversation_id>.bin"
}
```

**Response (error):**
```json
{
  "status": "error",
  "message": "Only .bin files are allowed"
}
```
or
```json
{
  "status": "error",
  "message": "Failed to save file: <error details>"
}
```

## API Documentation

Once the server is running, you can access the interactive API documentation at:
- Swagger UI: `http://localhost:8001/docs`
- ReDoc: `http://localhost:8001/redoc`