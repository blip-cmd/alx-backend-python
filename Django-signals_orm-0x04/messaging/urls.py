from django.urls import path
from . import views

app_name = "messaging"

urlpatterns = [
    # Main views
    path("", views.message_list, name="message_list"),
    path("send/", views.send_message, name="send_message"),
    path("notifications/", views.notifications_list, name="notifications"),
    # User management
    path("delete-account/", views.delete_user, name="delete_user"),
    # Message detail and editing
    path("message/<int:message_id>/", views.message_detail, name="message_detail"),
    path("message/<int:message_id>/edit/", views.edit_message, name="edit_message"),
    # API endpoints
    path(
        "api/message/<int:message_id>/history/",
        views.message_history_api,
        name="message_history_api",
    ),
    path(
        "api/notification/<int:notification_id>/read/",
        views.mark_notification_read,
        name="mark_notification_read",
    ),
]
