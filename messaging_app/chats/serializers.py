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
    Serializer for Message model, nested with sender details. Includes body validation.
    """
    sender = UserSerializer(read_only=True)
    message_body = serializers.CharField()
    sent_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Message
        fields = [
            'message_id', 'sender', 'message_body', 'sent_at', 'is_read'
        ]

    def validate_message_body(self, value):
        """
        Ensure the message body is not empty or whitespace only.
        """
        if not value.strip():
            raise serializers.ValidationError("Message body cannot be empty")
        return value


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for Conversation model, includes participants, nested messages,
    participant count, and group name validation.
    """
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    participant_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            'conversation_id', 'participants', 'participant_count',
            'name', 'is_group', 'created_at', 'messages'
        ]

    def get_participant_count(self, obj):
        """
        Return the number of participants in the conversation.
        """
        return obj.participants.count()

    def validate(self, data):
        """
        Ensure group conversations have a name.
        """
        if data.get('is_group') and not data.get('name'):
            raise serializers.ValidationError("Group conversations require a name")
        return data
