from rest_framework import serializers
from .models import CustomUser, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for CustomUser model.
    """
    class Meta:
        model = CustomUser
        fields = [
            'user_id', 'username', 'email', 'first_name', 'last_name', 'phone_number'
        ]


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for Message model, nested with sender details.
    """
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = [
            'message_id', 'sender', 'message_body', 'sent_at', 'is_read'
        ]


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for Conversation model, includes participants and nested messages.
    """
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = [
            'conversation_id', 'participants', 'name', 'is_group', 'created_at', 'messages'
        ]
