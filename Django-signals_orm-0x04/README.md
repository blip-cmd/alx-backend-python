# Django Signals for User Notifications

## Overview

This project implements a Django messaging system with automatic notification creation using Django signals. When a user receives a new message, a notification is automatically created for them.

## Features

- **Message Model**: Stores messages between users with sender, receiver, content, and timestamp
- **Notification Model**: Stores notifications linked to users and messages
- **Django Signals**: Automatically creates notifications when new messages are created
- **Admin Interface**: Full Django admin support for managing messages and notifications
- **Comprehensive Tests**: Unit and integration tests ensuring signal functionality

## Project Structure

```
messaging/
├── __init__.py          # App initialization and documentation
├── models.py            # Message and Notification models
├── signals.py           # Django signal handlers
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

### Notification
- `user`: ForeignKey to User (who receives the notification)
- `message`: ForeignKey to Message (the message that triggered the notification)
- `is_read`: BooleanField (whether notification has been read)
- `created_at`: DateTimeField (when notification was created)

## Signal Implementation

The `post_save` signal on the Message model automatically creates a Notification for the message receiver when a new message is created. This ensures users are always notified of new messages without manual intervention.

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
- Signal functionality and notification creation
- Edge cases like message updates and self-messaging

## Usage Example

```python
from django.contrib.auth.models import User
from messaging.models import Message, Notification

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
```

## Professional Development Practices

This implementation follows professional development practices:
- **Staged commits**: Each component was implemented and committed separately
- **Comprehensive documentation**: Clear docstrings and comments throughout
- **Test-driven approach**: Comprehensive test suite covering all functionality
- **Django best practices**: Proper model design, signal usage, and admin integration
- **Clean code**: Well-structured, readable, and maintainable code
