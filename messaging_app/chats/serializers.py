from rest_framework import serializers
from .models import User, Conversation, Message

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()
    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body', 'sent_at']

class UserSerializer(serializers.ModelSerializer):
    conversations = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    sent_messages = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = User
        fields = ['user_id', 'email', 'phone_number', 'role', 'created_at', 'conversations', 'sent_messages']

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'messages']
