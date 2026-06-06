from rest_framework import serializers

from .models import Conversation, Message


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for individual messages."""

    class Meta:
        model = Message
        fields = ['id', 'role', 'content', 'metadata', 'created_at']
        read_only_fields = ['id', 'created_at']


class ConversationListSerializer(serializers.ModelSerializer):
    """Serializer for listing conversations (summary view)."""

    message_count = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'title', 'created_at', 'updated_at', 'is_active', 'message_count', 'last_message']

    def get_message_count(self, obj):
        return obj.messages.count()

    def get_last_message(self, obj):
        last = obj.messages.order_by('-created_at').first()
        if last:
            return {
                "role": last.role,
                "preview": last.content[:100],
                "created_at": last.created_at,
            }
        return None


class ConversationDetailSerializer(serializers.ModelSerializer):
    """Serializer for conversation detail with all messages."""

    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['id', 'title', 'created_at', 'updated_at', 'is_active', 'messages']


class ChatInputSerializer(serializers.Serializer):
    """Validates user chat input."""

    message = serializers.CharField(max_length=5000)
    conversation_id = serializers.IntegerField(required=False, allow_null=True)
