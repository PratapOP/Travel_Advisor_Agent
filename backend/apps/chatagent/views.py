from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import ChatSession, ChatMessage
from .serializers import ChatSessionSerializer, ChatMessageSerializer
from ai_engine.agent import run_chat_agent

class ChatSessionListCreateView(generics.ListCreateAPIView):
    serializer_class = ChatSessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ChatSessionDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = ChatSessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user)

class ChatMessageCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, session_id):
        try:
            session = ChatSession.objects.get(pk=session_id, user=request.user)
        except ChatSession.DoesNotExist:
            return Response({"error": "Session not found"}, status=status.HTTP_404_NOT_FOUND)
            
        content = request.data.get('content', '').strip()
        if not content:
            return Response({"error": "Content cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)
            
        # Save user message
        user_msg = ChatMessage.objects.create(session=session, sender='user', content=content)
        
        # Compile recent chat history
        history_queryset = ChatMessage.objects.filter(session=session).order_by('created_at')
        history_list = []
        for msg in history_queryset:
            history_list.append({
                'role': 'user' if msg.sender == 'user' else 'assistant',
                'content': msg.content
            })
            
        # Execute AI Agent Response
        ai_response = run_chat_agent(history_list, request.user.profile)
        
        # Save AI response
        ai_msg = ChatMessage.objects.create(session=session, sender='ai', content=ai_response)
        
        # Update thread title if still generic
        if session.title == 'New Chat':
            session.title = content[:30] + ('...' if len(content) > 30 else '')
            session.save()
            
        return Response({
            "user_message": ChatMessageSerializer(user_msg).data,
            "ai_message": ChatMessageSerializer(ai_msg).data
        }, status=status.HTTP_201_CREATED)
