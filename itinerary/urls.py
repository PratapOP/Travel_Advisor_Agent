from django.urls import path

from . import views

urlpatterns = [
    path('', views.ItineraryListCreateView.as_view(), name='itinerary-list-create'),
    path('<int:pk>/', views.ItineraryDetailView.as_view(), name='itinerary-detail'),
    path('<int:pk>/generate/', views.AIGenerateItineraryView.as_view(), name='itinerary-ai-generate'),
]
