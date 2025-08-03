from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification


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
