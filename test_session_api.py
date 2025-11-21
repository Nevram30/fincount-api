"""
Test script for the session creation API
Run this after starting your FastAPI server
"""
import requests
import json
from datetime import datetime

# API endpoint
API_URL = "http://localhost:8000/sessions"

def test_session_without_userid():
    """Test creating a session without providing userId (should use default admin)"""
    print("\n" + "="*60)
    print("TEST 1: Creating session WITHOUT userId")
    print("="*60)
    
    payload = {
        "batchId": "test-batch-001",
        "species": "Tilapia",
        "location": "Cagangohan",
        "notes": "Test session without userId",
        "counts": {"Fish": 100},
        "timestamp": datetime.now().isoformat() + "Z",
        "imageUrl": ""
    }
    
    print(f"\nPayload:\n{json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(API_URL, json=payload)
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response:\n{json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 201:
            print("\n✅ SUCCESS: Session created with default admin user")
        else:
            print("\n❌ FAILED: Unexpected response")
            
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        print("Make sure the FastAPI server is running on http://localhost:8000")

def test_session_with_valid_userid():
    """Test creating a session with a valid userId"""
    print("\n" + "="*60)
    print("TEST 2: Creating session WITH valid userId")
    print("="*60)
    
    # Using the test user from database
    payload = {
        "batchId": "test-batch-002",
        "species": "Bangus (Milkfish)",
        "location": "Southern",
        "notes": "Test session with specific user",
        "counts": {"Fish": 50},
        "timestamp": datetime.now().isoformat() + "Z",
        "imageUrl": "",
        "userId": "30b72ff1-8666-415a-ab2e-998cc8f3b569"  # Test User
    }
    
    print(f"\nPayload:\n{json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(API_URL, json=payload)
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response:\n{json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 201:
            print("\n✅ SUCCESS: Session created with specified user")
        else:
            print("\n❌ FAILED: Unexpected response")
            
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")

def test_session_with_invalid_userid():
    """Test creating a session with an invalid userId (should fail with 404)"""
    print("\n" + "="*60)
    print("TEST 3: Creating session WITH invalid userId")
    print("="*60)
    
    payload = {
        "batchId": "test-batch-003",
        "species": "Tilapia",
        "location": "Cagangohan",
        "notes": "Test session with invalid user",
        "counts": {"Fish": 75},
        "timestamp": datetime.now().isoformat() + "Z",
        "imageUrl": "",
        "userId": "invalid-user-id-12345"
    }
    
    print(f"\nPayload:\n{json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(API_URL, json=payload)
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response:\n{json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 404:
            print("\n✅ SUCCESS: Correctly rejected invalid user with 404")
        else:
            print("\n❌ FAILED: Should have returned 404 for invalid user")
            
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("TESTING SESSION API - FOREIGN KEY FIX")
    print("="*60)
    print("\nMake sure your FastAPI server is running:")
    print("  uvicorn main:app --reload --port 8000")
    print("\nPress Enter to start tests...")
    input()
    
    # Run tests
    test_session_without_userid()
    test_session_with_valid_userid()
    test_session_with_invalid_userid()
    
    print("\n" + "="*60)
    print("TESTS COMPLETE")
    print("="*60 + "\n")
