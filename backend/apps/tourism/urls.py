from django.urls import path
from .views import TouristSpotListView, PhotoPoseListView

urlpatterns = [
    path('spots/', TouristSpotListView.as_view(), name='tourist_spots'),
    path('poses/', PhotoPoseListView.as_view(), name='photo_poses'),
]
