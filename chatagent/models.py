from django.conf import settings
from django.db import models


class Conversation(models.Model):
    """A chat conversation session between a user and the AI advisor."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='conversations',
    )
    title = models.CharField(max_length=255, default='New Conversation')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'conversations'
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.user.username}: {self.title}"

    def get_message_history(self, limit: int = 50) -> list[dict]:
        """Get conversation history formatted for the AI agent."""
        messages = self.messages.order_by('created_at')[:limit]
        return [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]


class Message(models.Model):
    """An individual message within a conversation."""

    ROLE_CHOICES = [
        ('user', 'User'),
        ('assistant', 'Assistant'),
        ('system', 'System'),
    ]

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages',
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    metadata = models.JSONField(
        default=dict, blank=True,
        help_text='Additional metadata (tools used, tokens, etc.)',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'messages'
        ordering = ['created_at']

    def __str__(self):
        preview = self.content[:50] + '...' if len(self.content) > 50 else self.content
        return f"[{self.role}] {preview}"
