"""
Messaging App - Django Signals Implementation

This Django app demonstrates the implementation of automatic user notifications
using Django signals. When a user receives a new message, a notification is
automatically created using the post_save signal.

Key Components:
- Message model: Stores messages between users
- Notification model: Stores notifications for users
- Signal handler: Automatically creates notifications when messages are created
- Admin interface: Provides management capabilities for messages and notifications
- Comprehensive tests: Ensures signal functionality works correctly

Usage:
1. Add 'messaging' to your INSTALLED_APPS in Django settings
2. Run migrations to create the database tables
3. Create messages through the Django admin or programmatically
4. Notifications will be automatically created for message receivers
"""

default_app_config = "messaging.apps.MessagingConfig"
