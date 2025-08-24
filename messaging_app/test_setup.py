#!/usr/bin/env python
"""
Simple test script to verify Django setup and run basic tests
"""
import os
import sys
import django
from django.test.utils import get_runner
from django.conf import settings

if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'messaging_app.settings')
    django.setup()
    
    # Basic check
    from django.core.management import execute_from_command_line
    
    # Check Django configuration
    print("Running Django check...")
    result = execute_from_command_line(['manage.py', 'check'])
    print("Django check completed successfully!")
    
    # Test imports
    print("Testing model imports...")
    from chats.models import User, Conversation, Message
    print("All models imported successfully!")
    
    print("Setup verification completed!")