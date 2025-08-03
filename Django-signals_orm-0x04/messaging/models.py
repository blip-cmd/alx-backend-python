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

    def edit_content(self, new_content, edited_by):
        """
        Edit the message content and create a history entry.

        Args:
            new_content (str): The new content for the message
            edited_by (User): The user making the edit
        """
        if self.content != new_content:
            # Create history entry before changing content
            MessageHistory.objects.create(
                message=self, old_content=self.content, edited_by=edited_by
            )
            # Update the message
            self.content = new_content
            self.edited = True
            self.save()


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
    edited_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="message_edits",
        help_text="User who made this edit",
    )
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
