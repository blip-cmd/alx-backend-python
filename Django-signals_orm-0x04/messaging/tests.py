from django.test import TestCase
from django.contrib.auth.models import User
from django.db import IntegrityError
from .models import Message, Notification, MessageHistory


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
        self.assertFalse(message.edited)  # Should be False by default

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


class MessageHistoryModelTest(TestCase):
    """Test cases for the MessageHistory model."""

    def setUp(self):
        """Set up test data for message history testing."""
        self.sender = User.objects.create_user(
            username="sender", email="sender@test.com", password="testpass123"
        )
        self.receiver = User.objects.create_user(
            username="receiver", email="receiver@test.com", password="testpass123"
        )
        self.message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Original message content",
        )

    def test_message_history_creation(self):
        """Test that a message history entry can be created successfully."""
        history = MessageHistory.objects.create(
            message=self.message,
            old_content="Previous content",
            edited_by=self.sender,
        )

        self.assertEqual(history.message, self.message)
        self.assertEqual(history.old_content, "Previous content")
        self.assertEqual(history.edited_by, self.sender)
        self.assertIsNotNone(history.edited_at)

    def test_message_history_str_representation(self):
        """Test the string representation of a message history."""
        history = MessageHistory.objects.create(
            message=self.message,
            old_content="Previous content",
            edited_by=self.sender,
        )

        expected_str = (
            f"History for message {self.message.id} - edited at {history.edited_at}"
        )
        self.assertEqual(str(history), expected_str)

    def test_message_history_relationship(self):
        """Test the relationship between Message and MessageHistory."""
        # Create multiple history entries
        for i in range(3):
            MessageHistory.objects.create(
                message=self.message,
                old_content=f"Content version {i}",
                edited_by=self.sender,
            )

        # Test the reverse relationship
        self.assertEqual(self.message.edit_history.count(), 3)

        # Test ordering (should be by -edited_at)
        histories = self.message.edit_history.all()
        for i in range(len(histories) - 1):
            self.assertGreaterEqual(histories[i].edited_at, histories[i + 1].edited_at)


class MessageEditSignalTest(TestCase):
    """Test cases for the Django signal that logs message edits."""

    def setUp(self):
        """Set up test users for signal testing."""
        self.sender = User.objects.create_user(
            username="sender", email="sender@test.com", password="testpass123"
        )
        self.receiver = User.objects.create_user(
            username="receiver", email="receiver@test.com", password="testpass123"
        )

    def test_message_history_created_on_edit(self):
        """Test that a history entry is created when a message is edited."""
        # Create a message
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Original content",
        )

        # Initially, there should be no history entries
        self.assertEqual(MessageHistory.objects.count(), 0)
        self.assertFalse(message.edited)

        # Edit the message
        message.content = "Edited content"
        message.save()

        # Check that a history entry was created
        self.assertEqual(MessageHistory.objects.count(), 1)

        # Verify the history details
        history = MessageHistory.objects.first()
        self.assertEqual(history.message, message)
        self.assertEqual(history.old_content, "Original content")

        # Verify the message is marked as edited
        message.refresh_from_db()
        self.assertTrue(message.edited)

    def test_no_history_created_on_same_content(self):
        """Test that no history is created when content doesn't change."""
        # Create a message
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Original content",
        )

        # Save the message again without changing content
        message.save()

        # Verify no history was created
        self.assertEqual(MessageHistory.objects.count(), 0)
        self.assertFalse(message.edited)

    def test_multiple_edits_create_multiple_histories(self):
        """Test that multiple edits create multiple history entries."""
        # Create a message
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Original content",
        )

        # Edit the message multiple times
        contents = ["First edit", "Second edit", "Third edit"]
        for i, content in enumerate(contents):
            message.content = content
            message.save()

            # Check that the correct number of history entries exist
            self.assertEqual(MessageHistory.objects.count(), i + 1)

        # Verify all history entries
        histories = MessageHistory.objects.order_by("edited_at")
        expected_contents = ["Original content", "First edit", "Second edit"]

        for i, history in enumerate(histories):
            self.assertEqual(history.old_content, expected_contents[i])

    def test_edit_content_method(self):
        """Test the custom edit_content method that tracks who made the edit."""
        # Create a message
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Original content",
        )

        # Initially, there should be no history entries
        self.assertEqual(MessageHistory.objects.count(), 0)
        self.assertFalse(message.edited)

        # Edit the message using the custom method
        message.edit_content("Edited content", self.sender)

        # Check that a history entry was created with the correct editor
        self.assertEqual(MessageHistory.objects.count(), 1)
        history = MessageHistory.objects.first()
        self.assertEqual(history.message, message)
        self.assertEqual(history.old_content, "Original content")
        self.assertEqual(history.edited_by, self.sender)

        # Verify the message is marked as edited and content updated
        message.refresh_from_db()
        self.assertTrue(message.edited)
        self.assertEqual(message.content, "Edited content")

    def test_edit_content_method_no_change(self):
        """Test that edit_content doesn't create history if content doesn't change."""
        # Create a message
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Original content",
        )

        # Try to "edit" with the same content
        message.edit_content("Original content", self.sender)

        # Verify no history was created
        self.assertEqual(MessageHistory.objects.count(), 0)
        self.assertFalse(message.edited)

    def test_no_history_on_new_message_creation(self):
        """Test that no history is created when a new message is created."""
        # Create a new message
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="New message content",
        )

        # Verify no history was created
        self.assertEqual(MessageHistory.objects.count(), 0)
        self.assertFalse(message.edited)

    def test_other_field_changes_dont_create_history(self):
        """Test that changing non-content fields doesn't create history."""
        # Create a message
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Original content",
        )

        # Change the edited field directly (simulating other operations)
        message.edited = True
        message.save()

        # Verify no history was created since content didn't change
        self.assertEqual(MessageHistory.objects.count(), 0)
