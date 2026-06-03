from rest_framework import serializers
from .models import Itinerary

class ItinerarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Itinerary
        fields = [
            'id', 
            'source', 
            'destination', 
            'num_days', 
            'budget_amount', 
            'interests', 
            'travel_style', 
            'day_wise_plan', 
            'created_at'
        ]
        read_only_fields = ['day_wise_plan', 'created_at']
