from django.urls import path

from . import views

urlpatterns = [
    path('recommendations/', views.HotelRecommendationListCreateView.as_view(), name='hotel-recommendation-list'),
    path('recommendations/<int:pk>/', views.HotelRecommendationDetailView.as_view(), name='hotel-recommendation-detail'),
    path('preferences/', views.HotelPreferenceView.as_view(), name='hotel-preferences'),
]
