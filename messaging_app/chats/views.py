from django.shortcuts import render
from rest_framework import viewsets, status, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
	"""
	API endpoint for listing, retrieving, creating, and updating conversations.
	Includes search and ordering functionality.
	"""
	queryset = Conversation.objects.all()
	serializer_class = ConversationSerializer
	permission_classes = [IsAuthenticated]
	filter_backends = [filters.SearchFilter, filters.OrderingFilter]
	search_fields = ['name', 'participants__username']
	ordering_fields = ['created_at']

	def perform_create(self, serializer):
		# Create the conversation instance
		conversation = serializer.save()
		# Always add the request user as a participant
		conversation.participants.add(self.request.user)
		# Add any other participants provided in the request
		participants_ids = self.request.data.get('participants', [])
		if participants_ids:
			conversation.participants.add(*participants_ids)
		# Return a custom response if needed
		return Response(self.get_serializer(conversation).data, status=status.HTTP_201_CREATED)



class MessageViewSet(viewsets.ModelViewSet):
	"""
	API endpoint for listing, retrieving, and sending messages.
	Supports filtering by conversation.
	"""
	queryset = Message.objects.all()
	serializer_class = MessageSerializer
	permission_classes = [IsAuthenticated]
	filter_backends = [filters.OrderingFilter]
	filterset_fields = ['conversation']
	ordering_fields = ['sent_at']

	def perform_create(self, serializer):
		# Automatically set the sender to the authenticated user
		message = serializer.save(sender=self.request.user)
		return Response(self.get_serializer(message).data, status=status.HTTP_201_CREATED)

