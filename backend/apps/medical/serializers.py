from rest_framework import serializers
from .models import MedicalGuidance

class MedicalGuidanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalGuidance
        fields = [
            'id', 
            'itinerary', 
            'questionnaire_responses', 
            'vaccinations', 
            'medicines', 
            'precautions', 
            'created_at'
        ]
        read_only_fields = ['id', 'itinerary', 'created_at']
