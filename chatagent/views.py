from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Conversation
from .serializers import (
    ChatInputSerializer,
    ConversationDetailSerializer,
    ConversationListSerializer,
)
from .services import ChatService


class ChatView(APIView):
    """Send a message to the AI travel advisor and get a response."""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChatInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = ChatService.process_message(
            user=request.user,
            message_text=serializer.validated_data['message'],
            conversation_id=serializer.validated_data.get('conversation_id'),
        )

        return Response(result, status=status.HTTP_200_OK)


class ConversationListView(generics.ListAPIView):
    """List all conversations for the authenticated user."""

    serializer_class = ConversationListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Conversation.objects.filter(
            user=self.request.user,
            is_active=True,
        )


class ConversationDetailView(generics.RetrieveDestroyAPIView):
    """Retrieve or delete a specific conversation."""

    serializer_class = ConversationDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Conversation.objects.filter(user=self.request.user)

    def perform_destroy(self, instance):
        # Soft delete — mark as inactive
        instance.is_active = False
        instance.save(update_fields=['is_active'])
