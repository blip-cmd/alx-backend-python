# Django Signals for User Notifications and Message Edit Tracking

## Overview

This project implements a comprehensive Django messaging system with automatic notification creation and complete message edit tracking using Django signals. The system features a beautiful web interface that allows users to view message edit history, track who made changes, and manage notifications efficiently.

## Features

- **Message Model**: Stores messages between users with sender, receiver, content, timestamp, and edit tracking
- **Notification Model**: Stores notifications linked to users and messages  
- **MessageHistory Model**: Maintains complete edit history with user tracking for who made each edit
- **Django Signals**: 
  - Automatically creates notifications when new messages are created
  - Logs message content before edits to preserve history with user attribution
- **Web Interface**: Beautiful, responsive UI for viewing and editing messages
  - Message list with edit indicators and quick editing
  - Detailed message view with complete edit timeline
  - Send message form with user selection
  - Notifications management
- **Admin Interface**: Full Django admin support for managing messages, notifications, and edit history
- **Comprehensive Tests**: Unit and integration tests ensuring all signal functionality

## Project Structure

```
messaging/
├── __init__.py          # App initialization and documentation
├── models.py            # Message, Notification, and MessageHistory models
├── signals.py           # Django signal handlers for notifications and edit tracking
├── views.py             # Web interface views for message management
├── urls.py              # URL configuration for web interface
├── apps.py              # App configuration for signal registration
├── admin.py             # Django admin configuration
├── tests.py             # Comprehensive test suite
└── templates/messaging/ # HTML templates for web interface
    ├── base.html        # Base template with Bootstrap styling
    ├── message_list.html # Message list with edit functionality
    ├── message_detail.html # Detailed view with edit history
    ├── send_message.html # Send new message form
    └── notifications.html # Notifications management
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
- `edited_by`: ForeignKey to User (who made this edit)
- `edited_at`: DateTimeField (when the message was edited)

## Web Interface Features

### Message Management
- **Message List**: View all sent and received messages with edit indicators
- **Quick Edit**: Edit messages directly from the list view via modal
- **Message Details**: View complete message information and edit history
- **Send Messages**: User-friendly form to send new messages

### Edit History Display
- **Timeline View**: Chronological display of all message edits
- **User Attribution**: See who made each edit and when
- **Content Comparison**: View previous versions alongside current content
- **Visual Indicators**: Clear badges and styling for edited messages

### Notifications
- **Auto-Creation**: Notifications automatically created for new messages
- **Read/Unread Status**: Track which notifications have been viewed
- **Mark as Read**: Individual and bulk marking functionality
- **Message Preview**: Quick preview of message content in notifications

## Signal Implementation

### Notification Creation
The `post_save` signal on the Message model automatically creates a Notification for the message receiver when a new message is created. This ensures users are always notified of new messages without manual intervention.

### Edit History Tracking
The `pre_save` signal on the Message model captures the original content before any edit and stores it in a MessageHistory entry. This provides a complete audit trail of all message modifications.

## Setup Instructions

1. Add `'messaging'` to your `INSTALLED_APPS` in Django settings
2. Add the messaging URLs to your main project's `urls.py`:
   ```python
   from django.urls import path, include
   
   urlpatterns = [
       path('admin/', admin.site.urls),
       path('messaging/', include('messaging.urls')),
   ]
   ```
3. Run migrations to create the database tables:
   ```bash
   python manage.py makemigrations messaging
   python manage.py migrate
   ```
4. Create a superuser: `python manage.py createsuperuser`
5. Create some test users through the Django admin
6. Access the messaging interface at `http://localhost:8000/messaging/`

## Web Interface Usage

### Accessing the System
- **Message List**: `http://localhost:8000/messaging/` - View all your messages
- **Send Message**: `http://localhost:8000/messaging/send/` - Send a new message
- **Notifications**: `http://localhost:8000/messaging/notifications/` - View notifications

### Viewing Edit History
1. Navigate to the message list
2. Click "View Details" on any message
3. If the message has been edited, you'll see the complete edit history
4. Each edit shows:
   - Who made the edit
   - When it was made
   - The previous content
   - Visual timeline of changes

### Editing Messages
1. Only message senders can edit their own messages
2. Click the "Edit" button on a message
3. Make your changes in the modal dialog
4. Previous content is automatically saved to history
5. The edit is attributed to you with a timestamp

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
editor = User.objects.create_user('admin', 'admin@example.com', 'password')

# Create a message (notification will be created automatically)
message = Message.objects.create(
    sender=sender,
    receiver=receiver,
    content="Hello Jane!"
)

# Check that notification was created
notification = Notification.objects.filter(user=receiver).first()
print(f"Notification created: {notification}")

# Edit the message using the recommended method (tracks who made the edit)
message.edit_content("Hello Jane! How are you doing today?", sender)

# Check edit history with user tracking
print(f"Message edited: {message.edited}")  # True
history = message.edit_history.first()
print(f"Previous content: {history.old_content}")  # "Hello Jane!"
print(f"Edited by: {history.edited_by.username}")  # "john"
print(f"Edited at: {history.edited_at}")

# Admin makes another edit
message.edit_content("Hi Jane! Hope you're having a great day!", editor)

# View all edit history with user attribution
for i, history in enumerate(message.edit_history.all(), 1):
    print(f"Edit {i}: {history.old_content}")
    print(f"  Edited by: {history.edited_by.username}")
    print(f"  Edited at: {history.edited_at}")
```

## Professional Development Practices

This implementation follows professional development practices:
- **Staged commits**: Each component was implemented and committed separately
- **Comprehensive documentation**: Clear docstrings and comments throughout
- **Test-driven approach**: Comprehensive test suite covering all functionality
- **Django best practices**: Proper model design, signal usage, and admin integration
- **Clean code**: Well-structured, readable, and maintainable code
