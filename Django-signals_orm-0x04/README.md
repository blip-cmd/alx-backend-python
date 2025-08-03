# Django Signals for User Notifications and Message Edit Tracking

## Overview

This project implements a Django messaging system with automatic notification creation and comprehensive message edit tracking using Django signals. When a user receives a new message, a notification is automatically created for them. Additionally, when messages are edited, the system maintains a complete history of previous versions.

## Features

- **Message Model**: Stores messages between users with sender, receiver, content, timestamp, and edit tracking
- **Notification Model**: Stores notifications linked to users and messages  
- **MessageHistory Model**: Maintains complete edit history for messages
- **Django Signals**: 
  - Automatically creates notifications when new messages are created
  - Logs message content before edits to preserve history
- **Admin Interface**: Full Django admin support for managing messages, notifications, and edit history
- **Comprehensive Tests**: Unit and integration tests ensuring all signal functionality

## Project Structure

```
messaging/
├── __init__.py          # App initialization and documentation
├── models.py            # Message, Notification, and MessageHistory models
├── signals.py           # Django signal handlers for notifications and edit tracking
├── apps.py              # App configuration for signal registration
├── admin.py             # Django admin configuration
└── tests.py             # Comprehensive test suite
```

## Models

### Message

- `sender`: ForeignKey to User (who sent the message)
- `receiver`: ForeignKey to User (who receives the message)
- `content`: TextField (message content)
- `timestamp`: DateTimeField (when message was created)
- `edited`: BooleanField (whether the message has been edited)

### Notification

- `user`: ForeignKey to User (who receives the notification)
- `message`: ForeignKey to Message (the message that triggered the notification)
- `is_read`: BooleanField (whether notification has been read)
- `created_at`: DateTimeField (when notification was created)

### MessageHistory

- `message`: ForeignKey to Message (the message this history belongs to)
- `old_content`: TextField (previous content of the message)
- `edited_at`: DateTimeField (when the message was edited)

## Signal Implementation

### Notification Creation
The `post_save` signal on the Message model automatically creates a Notification for the message receiver when a new message is created. This ensures users are always notified of new messages without manual intervention.

### Edit History Tracking
The `pre_save` signal on the Message model captures the original content before any edit and stores it in a MessageHistory entry. This provides a complete audit trail of all message modifications.

## Setup Instructions

1. Add `'messaging'` to your `INSTALLED_APPS` in Django settings
2. Run `python manage.py makemigrations messaging`
3. Run `python manage.py migrate`
4. Create a superuser: `python manage.py createsuperuser`
5. Access the Django admin to test the functionality

## Testing

Run the comprehensive test suite with:
```bash
python manage.py test messaging
```

The tests cover:

- Model creation and string representations
- Signal functionality for notification creation
- Signal functionality for message edit history tracking
- Edge cases like message updates, self-messaging, and multiple edits
- Relationship integrity between models

## Usage Example

```python
from django.contrib.auth.models import User
from messaging.models import Message, Notification, MessageHistory

# Create users
sender = User.objects.create_user('john', 'john@example.com', 'password')
receiver = User.objects.create_user('jane', 'jane@example.com', 'password')

# Create a message (notification will be created automatically)
message = Message.objects.create(
    sender=sender,
    receiver=receiver,
    content="Hello Jane!"
)

# Check that notification was created
notification = Notification.objects.filter(user=receiver).first()
print(f"Notification created: {notification}")

# Edit the message (history will be created automatically)
message.content = "Hello Jane! How are you doing today?"
message.save()

# Check edit history
print(f"Message edited: {message.edited}")  # True
history = message.edit_history.first()
print(f"Previous content: {history.old_content}")  # "Hello Jane!"
print(f"Edited at: {history.edited_at}")

# Edit again to see multiple history entries
message.content = "Hi Jane! Hope you're having a great day!"
message.save()

# View all edit history
for i, history in enumerate(message.edit_history.all(), 1):
    print(f"Edit {i}: {history.old_content}")
```

## Professional Development Practices

This implementation follows professional development practices:
- **Staged commits**: Each component was implemented and committed separately
- **Comprehensive documentation**: Clear docstrings and comments throughout
- **Test-driven approach**: Comprehensive test suite covering all functionality
- **Django best practices**: Proper model design, signal usage, and admin integration
- **Clean code**: Well-structured, readable, and maintainable code
