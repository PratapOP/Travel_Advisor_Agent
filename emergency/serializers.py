from rest_framework import serializers
from .models import EmergencyInfo

class EmergencyInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyInfo
        fields = ['id', 'destination', 'emergency_numbers', 'embassy_info', 'safety_tips', 'travel_warnings', 'ai_generated_at']
        read_only_fields = ['id', 'ai_generated_at']
