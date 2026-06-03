from rest_framework import serializers
from .models import ChatSession, ChatMessage

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'sender', 'content', 'created_at']
        read_only_fields = ['id', 'created_at']

class ChatSessionSerializer(serializers.ModelSerializer):
    messages = ChatMessageSerializer(many=True, read_only=True)

    class Meta:
        model = ChatSession
        fields = ['id', 'title', 'messages', 'created_at']
        read_only_fields = ['id', 'messages', 'created_at']
