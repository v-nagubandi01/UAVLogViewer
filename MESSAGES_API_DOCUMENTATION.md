# Messages Upload API Documentation

## Overview

This document describes the new `/upload-messages` API endpoint that receives parsed messages from the frontend after a .bin file has been processed.

## Backend Endpoint

### POST `/upload-messages`

Receives the parsed messages object from the frontend after all messages have been processed.

**Request Body:**
```json
{
  "conversation_id": "uuid-string",
  "messages": {
    "GPS": {
      "time_boot_ms": [100, 200, 300, ...],
      "Lat": [37.7749, 37.7750, ...],
      "Lng": [-122.4194, -122.4195, ...],
      "Alt": [100.5, 101.2, ...]
    },
    "ATT": {
      "time_boot_ms": [100, 200, 300, ...],
      "Roll": [0.1, 0.2, 0.3, ...],
      "Pitch": [0.05, 0.06, ...],
      "Yaw": [1.5, 1.6, ...]
    }
    // ... more message types
  }
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Successfully received N message types"
}
```

**Error Response:**
```json
{
  "status": "error",
  "message": "Error description"
}
```

## How It Works

### 1. File Upload Flow
1. User drops/selects a .bin file
2. Frontend generates a UUID `conversation_id`
3. File is uploaded to `/upload-data` endpoint
4. Backend parses file and creates session with `conversation_id`

### 2. Message Processing Flow
1. Frontend parses file in Web Worker
2. Messages are stored in `state.messages` object
3. `extractFlightData()` processes the messages
4. **NEW:** `sendMessagesToBackend()` is called automatically
5. Messages are sent to `/upload-messages` endpoint **only once**

### 3. Backend Storage
The messages are stored in the session:
```python
sessions[conversation_id]["frontend_messages"] = messages
```

Session metadata is updated:
```python
session_metadata[conversation_id]["frontend_messages_received"] = True
session_metadata[conversation_id]["message_types_count"] = total_message_types
session_metadata[conversation_id]["message_types"] = message_types
```

## Safety Features

✅ **Only called once** - `messagesSentToBackend` flag prevents duplicate sends
✅ **Only for .bin files** - Checks `logType === 'bin'`
✅ **Requires conversation ID** - Checks for valid `conversationId`
✅ **Non-blocking** - Errors don't break the frontend
✅ **Automatic reset** - Flag resets when new file is loaded

## State Management

### New Global State Property
Added to `Globals.js`:
```javascript
messagesSentToBackend: false  // Track if messages sent to backend
```

This flag is:
- Set to `true` after successful upload
- Reset to `false` when a new file is loaded
- Checked before sending to prevent duplicates

## Implementation Details

### Frontend Changes

**File: `src/components/Globals.js`**
- Added `messagesSentToBackend: false` to state

**File: `src/components/Home.vue`**
- Added `sendMessagesToBackend()` method
- Calls endpoint after `extractFlightData()` completes
- Converts typed arrays to regular arrays for JSON serialization

**File: `src/components/SideBarFileManager.vue`**
- Resets `messagesSentToBackend` flag when new file is loaded

### Backend Changes

**File: `backend/main.py`**
- Added `MessagesUploadRequest` Pydantic model
- Added `MessagesUploadResponse` Pydantic model
- Added `/upload-messages` POST endpoint
- Stores messages in session under `frontend_messages` key
- Updates session metadata with message statistics

## Data Format

### Typed Arrays
The frontend stores data in typed arrays (Float64Array, etc.) for memory efficiency. These are converted to regular arrays before sending:

```javascript
// Convert typed arrays to regular arrays
if (values && values.constructor && values.constructor.name.includes('Array')) {
    messagesForBackend[msgType][field] = Array.from(values)
}
```

### Message Structure
Each message type contains:
- `time_boot_ms`: Timestamps in milliseconds
- Multiple field arrays (lat, lng, roll, pitch, etc.)
- Instance variants (e.g., `GPS[0]`, `GPS[1]`)

## Console Output

The backend logs detailed information:
```
============================================================
Received /upload-messages request
Conversation ID: abc-123-def
============================================================

Received 45 message types:
  - ATT: 1523 entries
  - GPS[0]: 1234 entries
  - BARO: 2000 entries
  ...

Successfully stored messages for conversation abc-123-def
============================================================
```

## Usage Example

To access the messages in backend code:

```python
@app.post("/my-analysis")
async def analyze_messages(conversation_id: str):
    if conversation_id not in sessions:
        return {"error": "Session not found"}
    
    # Get the frontend messages
    frontend_messages = sessions[conversation_id].get("frontend_messages", {})
    
    # Access specific message type
    if "ATT" in frontend_messages:
        roll_data = frontend_messages["ATT"]["Roll"]
        pitch_data = frontend_messages["ATT"]["Pitch"]
        # Perform analysis...
    
    return {"result": "Analysis complete"}
```

## Testing

To test the implementation:
1. Start the backend server
2. Open the frontend
3. Upload a .bin file
4. Watch the browser console for "Sending messages to backend..."
5. Check backend console for the detailed log output
6. Verify message is only sent once (try reloading - flag should prevent duplicate sends)

