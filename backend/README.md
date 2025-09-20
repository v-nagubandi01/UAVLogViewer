# UAV Log Viewer Backend

A FastAPI backend for the UAV Log Viewer application that processes ArduPilot flight logs and provides AI-powered analysis through LangGraph agents.

## Features

- **ArduPilot Log Processing**: Parses `.bin` files using MAVLink protocol
- **AI-Powered Analysis**: Uses Google Gemini AI with LangGraph for intelligent log analysis
- **Conversation Management**: Maintains conversation context across multiple interactions
- **Real-time Processing**: Fast file upload and processing with optimized pandas operations
- **RESTful API**: Clean FastAPI endpoints with automatic documentation

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

3. Environment Configuration:
Create a `.env` file in the backend directory with the following variables:
```bash
# Google Gemini API Key (required for AI analysis)
GOOGLE_API_KEY=your_google_api_key_here
```

**Note**: You'll need a Google API key to use the Gemini AI features. Get one from [Google AI Studio](https://makersuite.google.com/app/apikey).

## Running the Server

Start the development server:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8001
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
Processes chat messages with AI-powered analysis of uploaded flight log data.

**Request Body:**
```json
{
  "message": "What was the maximum altitude during the flight?",
  "conversationId": "uuid-string"
}
```

**Response:**
```json
{
  "response": "Based on the GPS data in your flight log, the maximum altitude reached was 125.3 meters above sea level at timestamp 2024-01-08 09:45:23. This occurred during the autonomous flight phase..."
}
```

**Features:**
- AI-powered analysis using Google Gemini
- Context-aware responses based on uploaded flight data
- Support for complex queries about flight parameters, performance, and anomalies
- Markdown-formatted responses with detailed insights

**Error Response:**
```json
{
  "response": "Error: Conversation ID not found. Please upload data first."
}
```

### POST /upload-data
Uploads and processes ArduPilot `.bin` flight log files for AI analysis.

**Form Data:**
- `file`: The `.bin` file to upload (required)
- `conversation_id`: The conversation ID (required)

**Processing:**
- Validates file format (must be `.bin`)
- Parses MAVLink messages using pymavlink
- Extracts telemetry data into pandas DataFrames
- Stores processed data in memory for conversation context
- Creates conversation session for subsequent chat interactions

**Response (success):**
```json
{
  "status": "success",
  "message": "File processed as <filename>_<conversation_id>.bin"
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
  "message": "Failed to process file: <error details>"
}
```

**Supported Data Types:**
- GPS coordinates and altitude
- Attitude (roll, pitch, yaw)
- Vibration data
- Control tuning parameters
- Battery status
- And other MAVLink message types

## Project Structure

```
backend/
├── main.py                 # FastAPI application and endpoints
├── deepagent.py           # LangGraph agent configuration and AI logic
├── parser.py              # MAVLink log parsing utilities
├── message_information.py # Message type definitions and metadata
├── requirements.txt       # Python dependencies
├── pyproject.toml        # Project configuration and linting rules
├── langgraph.json        # LangGraph configuration
└── README.md             # This file
```

## Key Components

- **main.py**: FastAPI server with CORS middleware, chat and upload endpoints
- **deepagent.py**: AI agent using Google Gemini with specialized prompts for ArduPilot log analysis
- **parser.py**: Optimized MAVLink binary log parser using pymavlink
- **message_information.py**: Definitions for different MAVLink message types and their fields

## Dependencies

### Core Framework
- **FastAPI**: Modern web framework for building APIs
- **Uvicorn**: ASGI server for running the application

### AI and Language Processing
- **LangChain**: Framework for building AI applications
- **LangGraph**: State management for AI agents
- **Google Generative AI**: Gemini model integration
- **DeepAgents**: Specialized agent framework

### Data Processing
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **PyMAVLink**: MAVLink protocol implementation for drone communication

## API Documentation

Once the server is running, you can access the interactive API documentation at:
- Swagger UI: `http://localhost:8001/docs`
- ReDoc: `http://localhost:8001/redoc`

## Development

The backend uses Ruff for code formatting and linting. Configuration is in `pyproject.toml`.

```bash
# Format code
ruff format .

# Lint code
ruff check .
```
