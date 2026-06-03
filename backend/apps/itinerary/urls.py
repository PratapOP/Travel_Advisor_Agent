from django.urls import path
from .views import ItineraryListCreateView, ItineraryDetailView

urlpatterns = [
    path('', ItineraryListCreateView.as_view(), name='itinerary_list_create'),
    path('<int:pk>/', ItineraryDetailView.as_view(), name='itinerary_detail'),
]
