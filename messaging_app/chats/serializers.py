from rest_framework import serializers
from .models import User, Conversation, Message


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    conversation = serializers.PrimaryKeyRelatedField(queryset=Conversation.objects.all(), required=True)
    message_body = serializers.CharField()

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'conversation', 'message_body', 'sent_at']


class UserSerializer(serializers.ModelSerializer):
    conversations = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    sent_messages = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    email = serializers.CharField()
    role = serializers.CharField()

    class Meta:
        model = User
        fields = ['user_id', 'email', 'phone_number', 'role', 'created_at', 'conversations', 'sent_messages']


class ConversationSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())
    messages = MessageSerializer(many=True, read_only=True, source='messages')

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'messages']

    def validate_participants(self, value):
        if not value:
            raise serializers.ValidationError("At least one participant is required.")
        return value
