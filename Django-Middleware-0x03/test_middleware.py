#!/usr/bin/env python
"""
Test script to demonstrate Django middleware functionality.
Run this after starting the Django server to test the middleware.
"""

import os
import sys
import django

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'messaging_app.settings')

# Setup Django
django.setup()

from django.test import RequestFactory, Client
from django.contrib.auth import get_user_model
from chats.models import User, Conversation, Message

def test_middleware():
    """Test the middleware functionality."""
    print("Testing Django Middleware...")
    
    # Create a test client
    client = Client()
    
    print("\n1. Testing Request Logging Middleware:")
    print("Making a GET request to /chats/ - check requests.log for logging")
    response = client.get('/chats/')
    print(f"Response status: {response.status_code}")
    
    print("\n2. Testing Time Restriction Middleware:")
    print("The middleware restricts access outside 6AM-9PM")
    print("Current response status:", response.status_code)
    if response.status_code == 403:
        print("Access restricted due to time constraints")
    else:
        print("Access allowed within time constraints")
    
    print("\n3. Testing Rate Limiting Middleware:")
    print("Making multiple POST requests to test rate limiting...")
    for i in range(7):  # Exceed the 5 message limit
        response = client.post('/chats/messages/', {'message': f'Test message {i+1}'})
        print(f"Request {i+1}: Status {response.status_code}")
        if response.status_code == 429:
            print("Rate limit exceeded!")
            break
    
    print("\n4. Testing Role Permission Middleware:")
    print("Accessing admin endpoints without proper role...")
    response = client.get('/admin/')
    print(f"Admin access response: {response.status_code}")
    
    print("\nMiddleware testing completed!")
    print("Check requests.log file for detailed request logging.")

if __name__ == "__main__":
    test_middleware()