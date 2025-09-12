#!/usr/bin/env python3
"""
Simple test script to verify the FastAPI backend is working correctly.
"""

import requests
import json

def test_backend():
    base_url = "http://localhost:3001"
    
    print("Testing FastAPI Backend...")
    print("=" * 40)
    
    # Test root endpoint
    try:
        response = requests.get(f"{base_url}/")
        print(f"GET / - Status: {response.status_code}")
        print(f"Response: {response.json()}")
        print()
    except Exception as e:
        print(f"Error testing root endpoint: {e}")
        return
    
    # Test chat endpoint
    try:
        test_message = "Hello, this is a test message!"
        payload = {"message": test_message}
        response = requests.post(
            f"{base_url}/chat",
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload)
        )
        print(f"POST /chat - Status: {response.status_code}")
        print(f"Request: {payload}")
        print(f"Response: {response.json()}")
        print()
        
        # Verify the response format
        response_data = response.json()
        expected_response = f"You said: {test_message}"
        if response_data.get("response") == expected_response:
            print("✅ Chat endpoint working correctly!")
        else:
            print("❌ Chat endpoint response format incorrect")
            
    except Exception as e:
        print(f"Error testing chat endpoint: {e}")

if __name__ == "__main__":
    test_backend()
