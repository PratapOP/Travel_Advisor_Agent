from django.db import models
from django.contrib.auth.models import User

class ChatSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_sessions')
    title = models.CharField(max_length=255, default='New Chat')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.title} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"

class ChatMessage(models.Model):
    SENDER_CHOICES = (
        ('user', 'User'),
        ('ai', 'AI Agent'),
    )
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=10, choices=SENDER_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}: {self.content[:30]}..."
