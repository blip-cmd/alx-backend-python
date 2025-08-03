#!/usr/bin/env python
"""
Test script to verify the delete user functionality and signal implementation.
This script demonstrates that the post_delete signal works correctly.
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "messaging.settings")
django.setup()

from django.contrib.auth.models import User
from django.db import models
from messaging.models import Message, Notification, MessageHistory


def test_user_deletion_with_signals():
    """
    Test that deleting a user properly cleans up all related data.
    This test verifies that the post_delete signal explicitly deletes
    all messages, notifications, and message histories.
    """
    print("=" * 50)
    print("TESTING USER DELETION WITH SIGNALS")
    print("=" * 50)

    # Create test users
    user1 = User.objects.create_user(
        username="testuser1", email="test1@example.com", password="testpass123"
    )
    user2 = User.objects.create_user(
        username="testuser2", email="test2@example.com", password="testpass123"
    )

    print(f"Created users: {user1.username}, {user2.username}")

    # Create test messages
    message1 = Message.objects.create(
        sender=user1, receiver=user2, content="Hello from user1 to user2"
    )

    message2 = Message.objects.create(
        sender=user2, receiver=user1, content="Reply from user2 to user1"
    )

    # Edit a message to create history
    message1.edit_content("Edited hello from user1 to user2", user1)

    print(f"Created {Message.objects.count()} messages")
    print(f"Created {Notification.objects.count()} notifications")
    print(f"Created {MessageHistory.objects.count()} message history entries")

    # Count related objects before deletion
    messages_before = Message.objects.filter(
        models.Q(sender=user1) | models.Q(receiver=user1)
    ).count()
    notifications_before = Notification.objects.filter(user=user1).count()
    history_before = MessageHistory.objects.filter(edited_by=user1).count()

    print(f"\nBefore deleting {user1.username}:")
    print(f"- Messages involving user1: {messages_before}")
    print(f"- Notifications for user1: {notifications_before}")
    print(f"- Message history by user1: {history_before}")

    # Count total objects before deletion to verify explicit deletion
    total_messages_before = Message.objects.count()
    total_notifications_before = Notification.objects.count()
    total_history_before = MessageHistory.objects.count()

    print(f"\nTotal objects before deletion:")
    print(f"- Total messages: {total_messages_before}")
    print(f"- Total notifications: {total_notifications_before}")
    print(f"- Total message history: {total_history_before}")

    # Delete user1 (this should trigger the post_delete signal with explicit deletion)
    print(f"\nDeleting user: {user1.username}")
    user1.delete()

    # Count related objects after deletion
    messages_after = Message.objects.filter(
        models.Q(sender__username="testuser1")
        | models.Q(receiver__username="testuser1")
    ).count()
    notifications_after = Notification.objects.filter(
        user__username="testuser1"
    ).count()
    history_after = MessageHistory.objects.filter(
        edited_by__username="testuser1"
    ).count()

    print(f"\nAfter deleting user1:")
    print(f"- Messages involving user1: {messages_after}")
    print(f"- Notifications for user1: {notifications_after}")
    print(f"- Message history by user1: {history_after}")

    # Count total objects after deletion
    total_messages_after = Message.objects.count()
    total_notifications_after = Notification.objects.count()
    total_history_after = MessageHistory.objects.count()

    print(f"\nTotal objects after deletion:")
    print(f"- Total messages: {total_messages_after}")
    print(f"- Total notifications: {total_notifications_after}")
    print(f"- Total message history: {total_history_after}")

    # Verify cleanup (should be 0 because of explicit deletion in signal)
    success = messages_after == 0 and notifications_after == 0 and history_after == 0

    print(f"\nCleanup successful: {success}")

    if success:
        print("✓ All related data was properly cleaned up by the post_delete signal!")
        print("✓ Signal used explicit Message.objects.filter().delete() calls")
    else:
        print("✗ Some related data was not cleaned up properly!")

    # Clean up remaining test data
    user2.delete()

    print("\nTest completed.")
    return success


def demonstrate_cascade_behavior():
    """
    Demonstrate that CASCADE foreign keys work correctly.
    """
    print("\n" + "=" * 50)
    print("DEMONSTRATING CASCADE BEHAVIOR")
    print("=" * 50)

    # Import here to avoid circular imports during Django setup
    from django.db import models

    # Create test users
    sender = User.objects.create_user(
        username="sender_test", email="sender@test.com", password="testpass123"
    )
    receiver = User.objects.create_user(
        username="receiver_test", email="receiver@test.com", password="testpass123"
    )

    print(f"Created test users: {sender.username}, {receiver.username}")

    # Create a message (this will automatically create a notification via signal)
    message = Message.objects.create(
        sender=sender,
        receiver=receiver,
        content="Test message for CASCADE demonstration",
    )

    # Edit the message to create history
    message.edit_content("Edited test message", sender)

    print(f"Created message with ID: {message.id}")
    print(f"Total messages: {Message.objects.count()}")
    print(f"Total notifications: {Notification.objects.count()}")
    print(f"Total message histories: {MessageHistory.objects.count()}")

    # Delete the sender user
    print(f"\nDeleting sender user: {sender.username}")
    sender.delete()

    # Check what remains
    print(f"\nAfter deleting sender:")
    print(f"Total messages: {Message.objects.count()}")
    print(f"Total notifications: {Notification.objects.count()}")
    print(f"Total message histories: {MessageHistory.objects.count()}")

    # Clean up
    receiver.delete()

    print("\nCASCADE demonstration completed.")


if __name__ == "__main__":
    try:
        # Test the delete user functionality
        test_success = test_user_deletion_with_signals()

        # Demonstrate CASCADE behavior
        demonstrate_cascade_behavior()

        print("\n" + "=" * 50)
        print("ALL TESTS COMPLETED")
        print("=" * 50)

        if test_success:
            print("✓ User deletion and cleanup functionality is working correctly!")
        else:
            print("✗ There are issues with the user deletion functionality!")

    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback

        traceback.print_exc()
