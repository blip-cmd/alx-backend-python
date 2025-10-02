from rest_framework import serializers
from .models import User, Conversation, Message


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()
    conversation = serializers.PrimaryKeyRelatedField(queryset=Conversation.objects.all(), required=True)
    message_body = serializers.CharField()

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'conversation', 'message_body', 'sent_at']

    def get_sender(self, obj):
        """Return sender information"""
        return {
            'user_id': str(obj.sender.user_id),
            'email': obj.sender.email,
            'role': obj.sender.role
        }


class UserSerializer(serializers.ModelSerializer):
    conversations = serializers.SerializerMethodField()
    sent_messages = serializers.SerializerMethodField()
    email = serializers.CharField()
    role = serializers.CharField()

    class Meta:
        model = User
        fields = ['user_id', 'email', 'phone_number', 'role', 'created_at', 'conversations', 'sent_messages']

    def get_conversations(self, obj):
        """Return conversation IDs for this user"""
        return [str(conv.conversation_id) for conv in obj.conversations.all()]

    def get_sent_messages(self, obj):
        """Return message IDs sent by this user"""
        return [str(msg.message_id) for msg in obj.sent_messages.all()]


class ConversationSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'messages']

    def get_messages(self, obj):
        """Return detailed message information for this conversation"""
        return [
            {
                'message_id': str(msg.message_id),
                'sender': {
                    'user_id': str(msg.sender.user_id),
                    'email': msg.sender.email,
                    'role': msg.sender.role
                },
                'message_body': msg.message_body,
                'sent_at': msg.sent_at
            }
            for msg in obj.messages.all().order_by('sent_at')
        ]

    def validate_participants(self, value):
        if not value:
            raise serializers.ValidationError("At least one participant is required.")
        return value
