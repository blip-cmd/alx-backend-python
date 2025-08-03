from django.test import TestCase
from django.contrib.auth.models import User
from django.db import IntegrityError
from .models import Message, Notification


class MessageModelTest(TestCase):
    """Test cases for the Message model."""

    def setUp(self):
        """Set up test users for message testing."""
        self.sender = User.objects.create_user(
            username="sender", email="sender@test.com", password="testpass123"
        )
        self.receiver = User.objects.create_user(
            username="receiver", email="receiver@test.com", password="testpass123"
        )

    def test_message_creation(self):
        """Test that a message can be created successfully."""
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Hello, this is a test message!",
        )

        self.assertEqual(message.sender, self.sender)
        self.assertEqual(message.receiver, self.receiver)
        self.assertEqual(message.content, "Hello, this is a test message!")
        self.assertIsNotNone(message.timestamp)

    def test_message_str_representation(self):
        """Test the string representation of a message."""
        message = Message.objects.create(
            sender=self.sender, receiver=self.receiver, content="Test message"
        )

        expected_str = f"Message from {self.sender.username} to {self.receiver.username} at {message.timestamp}"
        self.assertEqual(str(message), expected_str)


class NotificationModelTest(TestCase):
    """Test cases for the Notification model."""

    def setUp(self):
        """Set up test data for notification testing."""
        self.sender = User.objects.create_user(
            username="sender", email="sender@test.com", password="testpass123"
        )
        self.receiver = User.objects.create_user(
            username="receiver", email="receiver@test.com", password="testpass123"
        )
        self.message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Test message for notification",
        )

    def test_notification_creation(self):
        """Test that a notification can be created successfully."""
        notification = Notification.objects.create(
            user=self.receiver, message=self.message
        )

        self.assertEqual(notification.user, self.receiver)
        self.assertEqual(notification.message, self.message)
        self.assertFalse(notification.is_read)  # Default should be False
        self.assertIsNotNone(notification.created_at)

    def test_notification_str_representation(self):
        """Test the string representation of a notification."""
        notification = Notification.objects.create(
            user=self.receiver, message=self.message
        )

        expected_str = f"Notification for {self.receiver.username} - Unread"
        self.assertEqual(str(notification), expected_str)

        # Test read notification
        notification.is_read = True
        notification.save()
        expected_str = f"Notification for {self.receiver.username} - Read"
        self.assertEqual(str(notification), expected_str)


class MessageSignalTest(TestCase):
    """Test cases for the Django signal that creates notifications."""

    def setUp(self):
        """Set up test users for signal testing."""
        self.sender = User.objects.create_user(
            username="sender", email="sender@test.com", password="testpass123"
        )
        self.receiver = User.objects.create_user(
            username="receiver", email="receiver@test.com", password="testpass123"
        )

    def test_notification_created_on_message_creation(self):
        """Test that a notification is automatically created when a message is created."""
        # Initially, there should be no notifications
        self.assertEqual(Notification.objects.count(), 0)

        # Create a new message
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="This should trigger a notification!",
        )

        # Check that a notification was created
        self.assertEqual(Notification.objects.count(), 1)

        # Verify the notification details
        notification = Notification.objects.first()
        self.assertEqual(notification.user, self.receiver)
        self.assertEqual(notification.message, message)
        self.assertFalse(notification.is_read)

    def test_no_notification_on_message_update(self):
        """Test that no additional notification is created when a message is updated."""
        # Create a message (this will create one notification)
        message = Message.objects.create(
            sender=self.sender, receiver=self.receiver, content="Original content"
        )

        # Verify one notification exists
        self.assertEqual(Notification.objects.count(), 1)

        # Update the message
        message.content = "Updated content"
        message.save()

        # Verify no additional notification was created
        self.assertEqual(Notification.objects.count(), 1)

    def test_multiple_messages_create_multiple_notifications(self):
        """Test that multiple messages create multiple notifications."""
        # Create multiple messages
        for i in range(3):
            Message.objects.create(
                sender=self.sender, receiver=self.receiver, content=f"Message {i + 1}"
            )

        # Verify that 3 notifications were created
        self.assertEqual(Notification.objects.count(), 3)

        # Verify all notifications are for the receiver
        notifications = Notification.objects.all()
        for notification in notifications:
            self.assertEqual(notification.user, self.receiver)

    def test_self_message_creates_notification(self):
        """Test that a user can send a message to themselves and get notified."""
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.sender,  # Same user
            content="Note to self",
        )

        # Check that a notification was still created
        self.assertEqual(Notification.objects.count(), 1)
        notification = Notification.objects.first()
        self.assertEqual(notification.user, self.sender)
        self.assertEqual(notification.message, message)
