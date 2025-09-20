# UAV Log Viewer Backend

A FastAPI backend for the UAV Log Viewer application that processes ArduPilot flight logs and provides AI-powered analysis through LangGraph agents.

## Features

- **ArduPilot Log Processing**: Parses `.bin` files using MAVLink protocol
- **AI-Powered Analysis**: Uses Google Gemini AI with LangGraph for intelligent log analysis
- **Advanced Session Management**: Robust conversation tracking with metadata and analytics
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

**Note**: You'll need a Google API key to use the Gemini AI features.

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

### GET /session-info
**Core Session Management Endpoint** - Returns comprehensive information about all active sessions, providing real-time visibility into the session management system.

**Response:**
```json
{
  "total_sessions": 2,
  "active_sessions": [
    {
      "session_id": "uuid-string-1",
      "filename": "flight_log_2024.bin",
      "message_count": 5,
      "number_of_user_questions": 3,
      "created_at": "2024-01-08 09:44:08"
    },
    {
      "session_id": "uuid-string-2", 
      "filename": "test_flight.bin",
      "message_count": 2,
      "number_of_user_questions": 1,
      "created_at": "2024-01-08 10:15:30"
    }
  ]
}
```

**Use Cases:**
- **Session Monitoring**: Real-time visibility into all active conversation sessions
- **User Engagement Analytics**: Track how many questions users ask per session
- **Debugging & Troubleshooting**: Complete session history for issue resolution
- **Performance Monitoring**: Analyze session usage patterns and system load
- **Conversation Management**: Monitor conversation flow and context preservation

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

## Agent Architecture

The UAV Log Viewer uses **DeepAgents**, a sophisticated AI framework that excels at handling complex conversations and can intelligently use subagents and tools to complete tasks. DeepAgents provides advanced state management and decision-making capabilities that make it ideal for analyzing flight log data.

### Available Tools

The agent has access to five specialized tools for flight log analysis:

1. **`select_message_types_tool`**: Intelligently selects relevant MAVLink message types (GPS, ATT, VIBE, etc.) based on the user's question and flight characteristics.

2. **`generate_pandas_code_tool`**: Creates optimized pandas code for data analysis, taking into account the selected message types, question context, and flight lifecycle behavior.

3. **`pandas_executor_tool`**: Executes the generated pandas code on the flight data and stores the results for further processing.

4. **`pandas_code_correction_tool`**: Automatically detects and fixes errors in pandas code execution, ensuring robust data analysis.

5. **`summarize_results_tool`**: Provides intelligent summarization of analysis results, presenting findings in a clear and actionable format.

### Example Conversations

#### Question 1: "What was the highest altitude reached during the flight?"

**Tool Flow:**
1. **Select Message Types Tool** → Identifies that GPS/POS messages contain altitude data
2. **Generate Pandas Tool** → Creates code to find maximum altitude, considering flight lifecycle and data collection patterns
3. **Execute Pandas Tool** → Runs the analysis and stores results
4. **Summarize Results Tool** → Formats the findings

**Final Answer:** "The highest altitude reached was 124.6 meters, which was extracted from the POS table at timestamp 2024-01-08 09:45:23 during the autonomous flight phase."

#### Question 2 (Follow-up): "Why did you look at the POS table?"

**Tool Flow:**
- **No tools called** → DeepAgent leverages conversation history and tool execution context to provide a contextual explanation

**Final Answer:** "I selected the POS table because it contains the most accurate GPS position data including altitude measurements. The POS messages are specifically designed for position reporting and provide higher precision altitude data compared to other message types like GPS, which may have different coordinate systems or update rates."

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

## Security Features

### CORS Configuration
The backend uses restrictive CORS settings for better security:

- **Allowed Origins**: Only specific frontend URLs (localhost:3000, localhost:3001, etc.)
- **Allowed Methods**: Only necessary HTTP methods (GET, POST, PUT, DELETE)
- **Allowed Headers**: Only required headers (Content-Type, Authorization, Accept)
- **Credentials**: Enabled for authenticated requests

**For Production**: Update the `allowed_origins` list in `main.py` to include your production frontend URL.

## Development

The backend uses Ruff for code formatting and linting. Configuration is in `pyproject.toml`.

```bash
# Format code
ruff format .

# Lint code
ruff check .
```
