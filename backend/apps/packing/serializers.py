from rest_framework import serializers
from .models import PackingList

class PackingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackingList
        fields = [
            'id', 
            'itinerary', 
            'weather_items', 
            'destination_items', 
            'medical_items', 
            'travel_documents', 
            'created_at'
        ]
        read_only_fields = ['id', 'itinerary', 'created_at']
