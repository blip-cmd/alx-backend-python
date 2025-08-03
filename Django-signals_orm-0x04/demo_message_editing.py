#!/usr/bin/env python
"""
Demo script to demonstrate message editing functionality.

This script shows how the MessageHistory model and signals work together
to track message edits automatically.

Note: This is a demonstration script. In a real Django project, you would
run this in a Django shell or as a management command.
"""

# This would typically be run in a Django shell or management command
# For demonstration purposes only


def demo_message_editing():
    """
    Demonstrates the message editing functionality.
    """
    print("=== Message Editing Demo ===\n")

    # This is pseudo-code to demonstrate the functionality
    # In a real Django environment, you would:

    print("1. Creating users...")
    # sender = User.objects.create_user('alice', 'alice@example.com', 'password')
    # receiver = User.objects.create_user('bob', 'bob@example.com', 'password')

    print("2. Creating initial message...")
    # message = Message.objects.create(
    #     sender=sender,
    #     receiver=receiver,
    #     content="Hello Bob! How are you doing today?"
    # )
    # print(f"Created message: {message.content}")
    # print(f"Message edited: {message.edited}")  # Should be False
    # print(f"History count: {message.edit_history.count()}")  # Should be 0

    print("\n3. Editing the message for the first time...")
    # message.content = "Hello Bob! How are you doing today? I hope you're well!"
    # message.save()
    # print(f"Updated message: {message.content}")
    # print(f"Message edited: {message.edited}")  # Should be True
    # print(f"History count: {message.edit_history.count()}")  # Should be 1

    print("\n4. Checking the edit history...")
    # history = message.edit_history.first()
    # print(f"Previous content: {history.old_content}")
    # print(f"Edited at: {history.edited_at}")

    print("\n5. Editing the message again...")
    # message.content = "Hi Bob! How are you? Hope you're having a great day!"
    # message.save()
    # print(f"Updated message: {message.content}")
    # print(f"History count: {message.edit_history.count()}")  # Should be 2

    print("\n6. Viewing all edit history...")
    # for i, history in enumerate(message.edit_history.all(), 1):
    #     print(f"Edit {i}: {history.old_content} (at {history.edited_at})")

    print("\n=== Demo Complete ===")
    print("\nKey Features Demonstrated:")
    print("- Messages track whether they've been edited")
    print("- Previous content is automatically saved before edits")
    print("- Complete edit history is maintained")
    print("- All functionality is handled by Django signals")


if __name__ == "__main__":
    demo_message_editing()
