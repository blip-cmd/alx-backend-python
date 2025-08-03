from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib import messages
from django.db.models import Q
from .models import Message, MessageHistory, Notification
import json


@login_required
def message_list(request):
    """
    Display a list of messages for the current user (sent and received).
    """
    messages = (
        Message.objects.filter(Q(sender=request.user) | Q(receiver=request.user))
        .select_related("sender", "receiver")
        .prefetch_related("edit_history")
    )

    context = {
        "messages": messages,
        "user": request.user,
    }
    return render(request, "messaging/message_list.html", context)


@login_required
def message_detail(request, message_id):
    """
    Display detailed view of a message including its edit history.
    """
    message = get_object_or_404(Message, id=message_id)

    # Check if user has permission to view this message
    if message.sender != request.user and message.receiver != request.user:
        return HttpResponseForbidden("You don't have permission to view this message.")

    # Get edit history
    edit_history = message.edit_history.all().select_related("edited_by")

    context = {
        "message": message,
        "edit_history": edit_history,
        "user": request.user,
        "can_edit": message.sender == request.user,  # Only sender can edit
    }
    return render(request, "messaging/message_detail.html", context)


@login_required
@require_POST
def edit_message(request, message_id):
    """
    Edit a message content (AJAX endpoint).
    """
    try:
        message = get_object_or_404(Message, id=message_id)

        # Check if user has permission to edit this message
        if message.sender != request.user:
            return JsonResponse(
                {"success": False, "error": "You can only edit your own messages."},
                status=403,
            )

        data = json.loads(request.body)
        new_content = data.get("content", "").strip()

        if not new_content:
            return JsonResponse(
                {"success": False, "error": "Message content cannot be empty."},
                status=400,
            )

        # Use the custom edit method to track who made the edit
        message.edit_content(new_content, request.user)

        return JsonResponse(
            {
                "success": True,
                "message": "Message updated successfully.",
                "new_content": new_content,
                "edited": message.edited,
            }
        )

    except json.JSONDecodeError:
        return JsonResponse(
            {"success": False, "error": "Invalid JSON data."}, status=400
        )
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@login_required
def message_history_api(request, message_id):
    """
    API endpoint to get message edit history (AJAX).
    """
    message = get_object_or_404(Message, id=message_id)

    # Check if user has permission to view this message
    if message.sender != request.user and message.receiver != request.user:
        return JsonResponse(
            {"error": "You don't have permission to view this message."}, status=403
        )

    history = []
    for entry in message.edit_history.all().select_related("edited_by"):
        history.append(
            {
                "id": entry.id,
                "old_content": entry.old_content,
                "edited_by": entry.edited_by.username,
                "edited_at": entry.edited_at.isoformat(),
                "edited_at_formatted": entry.edited_at.strftime("%Y-%m-%d %H:%M:%S"),
            }
        )

    return JsonResponse(
        {
            "history": history,
            "current_content": message.content,
            "is_edited": message.edited,
        }
    )


@login_required
def send_message(request):
    """
    Send a new message to another user.
    """
    if request.method == "POST":
        receiver_username = request.POST.get("receiver_username")
        content = request.POST.get("content", "").strip()

        if not receiver_username or not content:
            context = {
                "error": "Both receiver and content are required.",
                "users": User.objects.exclude(id=request.user.id),
            }
            return render(request, "messaging/send_message.html", context)

        try:
            receiver = User.objects.get(username=receiver_username)
            message = Message.objects.create(
                sender=request.user, receiver=receiver, content=content
            )

            context = {
                "success": f"Message sent to {receiver.username} successfully!",
                "users": User.objects.exclude(id=request.user.id),
            }
            return render(request, "messaging/send_message.html", context)

        except User.DoesNotExist:
            context = {
                "error": f'User "{receiver_username}" not found.',
                "users": User.objects.exclude(id=request.user.id),
            }
            return render(request, "messaging/send_message.html", context)

    context = {"users": User.objects.exclude(id=request.user.id)}
    return render(request, "messaging/send_message.html", context)


@login_required
def notifications_list(request):
    """
    Display notifications for the current user.
    """
    notifications = Notification.objects.filter(user=request.user).select_related(
        "message__sender"
    )

    context = {
        "notifications": notifications,
    }
    return render(request, "messaging/notifications.html", context)


@login_required
@require_POST
def mark_notification_read(request, notification_id):
    """
    Mark a notification as read (AJAX endpoint).
    """
    try:
        notification = get_object_or_404(
            Notification, id=notification_id, user=request.user
        )
        notification.is_read = True
        notification.save()

        return JsonResponse(
            {"success": True, "message": "Notification marked as read."}
        )
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@login_required
def delete_user(request):
    """
    Delete the current user's account and all associated data.

    This view allows users to delete their own account. When a user is deleted,
    the post_delete signal will automatically clean up related data due to
    CASCADE foreign key constraints.
    """
    if request.method == "POST":
        # Get confirmation from the form
        confirmation = request.POST.get("confirmation", "").strip().lower()

        if confirmation == "delete":
            user = request.user
            username = user.username

            try:
                # Log out the user before deletion
                logout(request)

                # Delete the user (this will trigger the post_delete signal)
                # and cascade delete all related data
                user.delete()

                # Add a success message for the redirect
                messages.success(
                    request, f"Account '{username}' has been successfully deleted."
                )

                # Redirect to a success page or home page
                return redirect("messaging:message_list")

            except Exception as e:
                messages.error(
                    request, f"An error occurred while deleting your account: {str(e)}"
                )
                return render(
                    request,
                    "messaging/delete_user.html",
                    {
                        "error": f"An error occurred while deleting your account: {str(e)}"
                    },
                )
        else:
            # Confirmation didn't match
            return render(
                request,
                "messaging/delete_user.html",
                {"error": "Please type 'delete' to confirm account deletion."},
            )

    # GET request - show the confirmation form
    return render(request, "messaging/delete_user.html")
