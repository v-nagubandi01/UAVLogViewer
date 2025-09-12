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
uvicorn main:app --reload --port 3001
```

The server will be available at `http://localhost:3001`

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

## Testing

Run the test script to verify the API is working:
```bash
python test_api.py
```

## API Documentation

Once the server is running, you can access the interactive API documentation at:
- Swagger UI: `http://localhost:3001/docs`
- ReDoc: `http://localhost:3001/redoc`
