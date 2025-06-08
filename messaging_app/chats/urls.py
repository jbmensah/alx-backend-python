from django.urls import path, include
from rest_framework import routers
from rest_framework_nested import routers as nested_routers
from .views import ConversationViewSet, MessageViewSet

# Top-level router for conversations
router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversations')

# Nested router so messages live under a specific conversation
nested_router = nested_routers.NestedDefaultRouter(router, r'conversations', lookup='conversation')
nested_router.register(r'messages', MessageViewSet, basename='conversation-messages')

urlpatterns = [
    # e.g. GET /api/conversations/, POST /api/conversations/
    path('', include(router.urls)),
    # e.g. GET /api/conversations/{conversation_pk}/messages/
    path('', include(nested_router.urls)),
]
