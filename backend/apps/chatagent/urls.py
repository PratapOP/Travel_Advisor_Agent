from django.urls import path
from .views import ChatSessionListCreateView, ChatSessionDetailView, ChatMessageCreateView

urlpatterns = [
    path('sessions/', ChatSessionListCreateView.as_view(), name='chat_sessions'),
    path('sessions/<int:pk>/', ChatSessionDetailView.as_view(), name='chat_session_detail'),
    path('sessions/<int:session_id>/message/', ChatMessageCreateView.as_view(), name='chat_message_create'),
]
