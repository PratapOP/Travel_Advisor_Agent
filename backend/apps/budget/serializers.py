from rest_framework import serializers
from .models import TripBudget

class TripBudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripBudget
        fields = [
            'id', 
            'itinerary', 
            'total_cost', 
            'accommodation_cost', 
            'food_budget', 
            'transport_budget', 
            'emergency_reserve', 
            'created_at'
        ]
        read_only_fields = ['id', 'itinerary', 'created_at']
