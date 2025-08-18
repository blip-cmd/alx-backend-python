
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['conversation_id', 'participants']
    permission_classes = [IsParticipantOfConversation]

    def create(self, request, *args, **kwargs):
        participants_ids = request.data.get('participants', [])
        if not participants_ids:
            return Response({'error': 'Participants required'}, status=status.HTTP_400_BAD_REQUEST)
        participants = User.objects.filter(user_id__in=participants_ids)
        if not participants.exists():
            return Response({'error': 'No valid participants found'}, status=status.HTTP_400_BAD_REQUEST)
        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['message_id', 'sender', 'conversation', 'message_body']
    permission_classes = [IsParticipantOfConversation]

    def create(self, request, *args, **kwargs):
        sender_id = request.data.get('sender')
        conversation_id = request.data.get('conversation')
        message_body = request.data.get('message_body')
        if not sender_id or not conversation_id or not message_body:
            return Response({'error': 'sender, conversation, and message_body required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            sender = User.objects.get(user_id=sender_id)
            conversation = Conversation.objects.get(conversation_id=conversation_id)
        except (User.DoesNotExist, Conversation.DoesNotExist):
            return Response({'error': 'Invalid sender or conversation'}, status=status.HTTP_400_BAD_REQUEST)
        message = Message.objects.create(sender=sender, conversation=conversation, message_body=message_body)
        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
