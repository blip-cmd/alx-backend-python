from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory


@receiver(post_save, sender=Message)
def create_notification_for_new_message(sender, instance, created, **kwargs):
    """
    Signal handler that creates a notification when a new message is created.

    Args:
        sender: The model class (Message)
        instance: The actual instance being saved (Message instance)
        created: Boolean indicating if this is a new instance
        **kwargs: Additional keyword arguments
    """
    if created:
        # Create notification for the message receiver
        Notification.objects.create(user=instance.receiver, message=instance)

        # Optional: Log the notification creation for debugging
        print(
            f"Notification created for {instance.receiver.username} "
            f"about message from {instance.sender.username}"
        )


@receiver(pre_save, sender=Message)
def log_message_edit_history(sender, instance, **kwargs):
    """
    Signal handler that logs the old content of a message before it's updated.
    Creates a MessageHistory entry when a message is edited.

    Note: This signal handler is kept for backward compatibility.
    For better tracking of who made the edit, use the Message.edit_content() method.

    Args:
        sender: The model class (Message)
        instance: The actual instance being saved (Message instance)
        **kwargs: Additional keyword arguments
    """
    # Only proceed if this is an update (not a new message)
    if instance.pk:
        try:
            # Get the current version from database
            old_message = Message.objects.get(pk=instance.pk)

            # Check if content has changed
            if old_message.content != instance.content:
                # Try to get edited_by from instance (if set by edit_content method)
                edited_by = getattr(instance, "_edited_by", None)

                if edited_by:
                    # Create history entry with user information
                    MessageHistory.objects.create(
                        message=old_message,
                        old_content=old_message.content,
                        edited_by=edited_by,
                    )
                else:
                    # Fallback: Use message sender as editor for backward compatibility
                    MessageHistory.objects.create(
                        message=old_message,
                        old_content=old_message.content,
                        edited_by=old_message.sender,
                    )

                # Mark the message as edited
                instance.edited = True

                # Optional: Log the edit for debugging
                editor = (
                    edited_by.username if edited_by else old_message.sender.username
                )
                print(
                    f"Message {instance.pk} edited by {editor}. "
                    f"Previous content saved to history."
                )
        except Message.DoesNotExist:
            # This shouldn't happen, but handle gracefully
            pass


@receiver(post_delete, sender=User)
def cleanup_user_related_data(sender, instance, **kwargs):
    """
    Signal handler that cleans up related data when a user is deleted.

    This signal explicitly deletes all messages, notifications, and message histories
    associated with the user to ensure complete cleanup.

    Args:
        sender: The model class (User)
        instance: The actual instance being deleted (User instance)
        **kwargs: Additional keyword arguments
    """
    username = instance.username

    # Log the cleanup for debugging/auditing
    print(f"Cleaning up data for deleted user: {username}")

    # Delete all messages where user is sender
    sent_messages = Message.objects.filter(sender=instance)
    sent_count = sent_messages.count()
    sent_messages.delete()
    print(f"Deleted {sent_count} sent messages")

    # Delete all messages where user is receiver
    received_messages = Message.objects.filter(receiver=instance)
    received_count = received_messages.count()
    received_messages.delete()
    print(f"Deleted {received_count} received messages")

    # Delete all notifications for the user
    user_notifications = Notification.objects.filter(user=instance)
    notification_count = user_notifications.count()
    user_notifications.delete()
    print(f"Deleted {notification_count} notifications")

    # Delete all message edit history where user was the editor
    user_edits = MessageHistory.objects.filter(edited_by=instance)
    edit_count = user_edits.count()
    user_edits.delete()
    print(f"Deleted {edit_count} message edit history entries")

    # Log completion
    print(f"Cleanup completed for user: {username}")
