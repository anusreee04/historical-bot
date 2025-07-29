#!/usr/bin/env python
"""
Test script to verify that chat history is being saved to the database.
This script will make a test API call and then check if the data was saved.
"""

import os
import sys
import django
import requests
import json

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from characters.models import ChatHistory

def test_chat_history_saving():
    """Test that chat history is being saved to the database"""
    
    # Get initial count of chat history records
    initial_count = ChatHistory.objects.count()
    print(f"Initial chat history count: {initial_count}")
    
    # Make a test API call to the chat endpoint
    url = "http://127.0.0.1:8000/api/chat/"
    test_data = {
        "character": "mahatma gandhi",
        "message": "What is your philosophy on non-violence?"
    }
    
    try:
        print("Making test API call...")
        response = requests.post(url, json=test_data, timeout=30)
        
        if response.status_code == 200:
            print("✅ API call successful!")
            response_data = response.json()
            print(f"Character: {response_data.get('character')}")
            print(f"Reply: {response_data.get('reply')[:100]}...")
            
            # Check if chat history was saved
            new_count = ChatHistory.objects.count()
            print(f"New chat history count: {new_count}")
            
            if new_count > initial_count:
                print("✅ Chat history was successfully saved to database!")
                
                # Get the latest chat history record
                latest_chat = ChatHistory.objects.latest('timestamp')
                print(f"Latest chat record:")
                print(f"  - Character: {latest_chat.character_name}")
                print(f"  - User Question: {latest_chat.user_question}")
                print(f"  - Bot Response: {latest_chat.bot_response[:100]}...")
                print(f"  - Timestamp: {latest_chat.timestamp}")
                
                return True
            else:
                print("❌ Chat history was NOT saved to database!")
                return False
        else:
            print(f"❌ API call failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error making API call: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_chat_history_api():
    """Test the chat history retrieval API"""
    
    url = "http://127.0.0.1:8000/api/chat-history/"
    
    try:
        print("\nTesting chat history API...")
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            print("✅ Chat history API call successful!")
            data = response.json()
            print(f"Total chat history records: {data.get('total_count', 0)}")
            
            if data.get('chat_history'):
                print("Recent chat history:")
                for i, chat in enumerate(data['chat_history'][:3]):  # Show first 3
                    print(f"  {i+1}. {chat['character_name']}: {chat['user_question'][:50]}...")
            
            return True
        else:
            print(f"❌ Chat history API call failed with status code: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error making chat history API call: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Chat History Functionality")
    print("=" * 50)
    
    # Test chat saving
    chat_save_success = test_chat_history_saving()
    
    # Test chat history retrieval
    chat_api_success = test_chat_history_api()
    
    print("\n" + "=" * 50)
    if chat_save_success and chat_api_success:
        print("🎉 All tests passed! Chat history is working correctly.")
    else:
        print("❌ Some tests failed. Please check the implementation.")
