from rest_framework import serializers
from .models import TouristSpot, PhotoPose

class TouristSpotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TouristSpot
        fields = [
            'id', 
            'name', 
            'city', 
            'country', 
            'description', 
            'category', 
            'rating', 
            'image_url'
        ]

class PhotoPoseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoPose
        fields = ['id', 'category', 'description', 'image_reference']
