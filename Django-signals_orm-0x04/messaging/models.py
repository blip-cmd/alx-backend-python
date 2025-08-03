from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Message(models.Model):
    """
    Model representing a message sent between users.
    """

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_messages",
        help_text="User who sent the message",
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="received_messages",
        help_text="User who receives the message",
    )
    content = models.TextField(help_text="Content of the message")
    timestamp = models.DateTimeField(
        default=timezone.now, help_text="When the message was created"
    )
    edited = models.BooleanField(
        default=False, help_text="Whether the message has been edited"
    )

    class Meta:
        ordering = ["-timestamp"]
        verbose_name = "Message"
        verbose_name_plural = "Messages"

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username} at {self.timestamp}"


class MessageHistory(models.Model):
    """
    Model representing the edit history of messages.
    Stores previous versions of message content when edited.
    """

    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name="edit_history",
        help_text="The message this history entry belongs to",
    )
    old_content = models.TextField(help_text="Previous content of the message")
    edited_at = models.DateTimeField(
        default=timezone.now, help_text="When the message was edited"
    )

    class Meta:
        ordering = ["-edited_at"]
        verbose_name = "Message History"
        verbose_name_plural = "Message Histories"

    def __str__(self):
        return f"History for message {self.message.id} - edited at {self.edited_at}"


class Notification(models.Model):
    """
    Model representing a notification for users.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications",
        help_text="User who receives the notification",
    )
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name="notifications",
        help_text="Message that triggered this notification",
    )
    is_read = models.BooleanField(
        default=False, help_text="Whether the notification has been read"
    )
    created_at = models.DateTimeField(
        default=timezone.now, help_text="When the notification was created"
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"

    def __str__(self):
        status = "Read" if self.is_read else "Unread"
        return f"Notification for {self.user.username} - {status}"
