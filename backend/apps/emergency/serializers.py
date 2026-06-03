from rest_framework import serializers
from .models import EmergencyContact

class EmergencyContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyContact
        fields = [
            'emergency_id', 
            'country', 
            'city', 
            'police_contact', 
            'ambulance_contact', 
            'tourist_helpline', 
            'embassy_contact'
        ]
