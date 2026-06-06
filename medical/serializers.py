from rest_framework import serializers
from .models import MedicalInfo, UserMedicalProfile

class MedicalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalInfo
        fields = [
            'id', 'destination', 'required_vaccinations', 
            'recommended_vaccinations', 'health_risks', 
            'insurance_recommendations', 'advisory_notes', 'ai_generated_at'
        ]
        read_only_fields = ['id', 'ai_generated_at']


class UserMedicalProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMedicalProfile
        fields = [
            'allergies', 'medications', 'blood_type', 
            'medical_conditions', 'emergency_contact_name', 'emergency_contact_phone'
        ]
