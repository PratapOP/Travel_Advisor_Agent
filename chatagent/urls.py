from django.urls import path

from . import views

urlpatterns = [
    path('send/', views.ChatView.as_view(), name='chat-send'),
    path('conversations/', views.ConversationListView.as_view(), name='conversation-list'),
    path('conversations/<int:pk>/', views.ConversationDetailView.as_view(), name='conversation-detail'),
]
