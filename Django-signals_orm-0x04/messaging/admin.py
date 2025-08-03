from django.contrib import admin
from .models import Message, Notification, MessageHistory


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """
    Admin configuration for Message model.
    """

    list_display = ("sender", "receiver", "content_preview", "timestamp", "edited")
    list_filter = ("timestamp", "sender", "receiver", "edited")
    search_fields = ("sender__username", "receiver__username", "content")
    readonly_fields = ("timestamp", "edited")
    ordering = ("-timestamp",)

    def content_preview(self, obj):
        """Return a truncated version of the message content."""
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content

    content_preview.short_description = "Content Preview"


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """
    Admin configuration for Notification model.
    """

    list_display = ("user", "message_preview", "is_read", "created_at")
    list_filter = ("is_read", "created_at", "user")
    search_fields = ("user__username", "message__content")
    readonly_fields = ("created_at", "message")
    ordering = ("-created_at",)

    def message_preview(self, obj):
        """Return a preview of the associated message."""
        return f"From {obj.message.sender.username}: {obj.message.content[:30]}..."

    message_preview.short_description = "Message Preview"

    actions = ["mark_as_read", "mark_as_unread"]

    def mark_as_read(self, request, queryset):
        """Mark selected notifications as read."""
        updated = queryset.update(is_read=True)
        self.message_user(request, f"{updated} notification(s) marked as read.")

    mark_as_read.short_description = "Mark selected notifications as read"

    def mark_as_unread(self, request, queryset):
        """Mark selected notifications as unread."""
        updated = queryset.update(is_read=False)
        self.message_user(request, f"{updated} notification(s) marked as unread.")

    mark_as_unread.short_description = "Mark selected notifications as unread"


class MessageHistoryInline(admin.TabularInline):
    """
    Inline admin for MessageHistory to show edit history within Message admin.
    """

    model = MessageHistory
    extra = 0
    readonly_fields = ("old_content", "edited_at")
    fields = ("old_content", "edited_at")
    ordering = ("-edited_at",)


@admin.register(MessageHistory)
class MessageHistoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for MessageHistory model.
    """

    list_display = ("message_preview", "content_preview", "edited_at")
    list_filter = ("edited_at",)
    search_fields = ("message__content", "old_content")
    readonly_fields = ("message", "old_content", "edited_at")
    ordering = ("-edited_at",)

    def message_preview(self, obj):
        """Return a preview of the associated message."""
        return f"Message {obj.message.id} from {obj.message.sender.username}"

    message_preview.short_description = "Message"

    def content_preview(self, obj):
        """Return a truncated version of the old content."""
        return (
            obj.old_content[:50] + "..."
            if len(obj.old_content) > 50
            else obj.old_content
        )

    content_preview.short_description = "Old Content"


# Update MessageAdmin to include history inline
MessageAdmin.inlines = [MessageHistoryInline]
