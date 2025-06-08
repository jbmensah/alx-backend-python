from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for listing, retrieving, creating, and updating conversations.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Create the conversation instance
        conversation = serializer.save()
        # Always add the request user as a participant
        conversation.participants.add(self.request.user)
        # Add any other participants provided in the request
        participants_ids = self.request.data.get('participants', [])
        if participants_ids:
            conversation.participants.add(*participants_ids)


class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint for listing, retrieving, and sending messages.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically set the sender to the authenticated user
        serializer.save(sender=self.request.user)

