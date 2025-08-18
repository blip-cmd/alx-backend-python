
from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allows only participants of a conversation to access/modify messages/conversations.
    """
    def has_object_permission(self, request, view, obj):
        # Allow safe methods for participants
        if hasattr(obj, 'participants'):
            is_participant = request.user in obj.participants.all()
        elif hasattr(obj, 'conversation'):
            is_participant = request.user in obj.conversation.participants.all()
        else:
            is_participant = False

        if request.method in permissions.SAFE_METHODS:
            return is_participant
        # For PUT, PATCH, DELETE, only participants can modify
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return is_participant
        return is_participant
