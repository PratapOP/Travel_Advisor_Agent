from rest_framework import serializers
from .models import TourismInfo, Attraction

class AttractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attraction
        fields = ['id', 'name', 'category', 'description', 'entry_fee', 'opening_hours', 'rating']


class TourismInfoSerializer(serializers.ModelSerializer):
    attractions = AttractionSerializer(many=True, read_only=True)

    class Meta:
        model = TourismInfo
        fields = [
            'id', 'destination', 'local_customs', 'language_tips', 
            'currency_info', 'best_time_to_visit', 'safety_rating', 
            'visa_requirements', 'attractions', 'ai_generated_at'
        ]
        read_only_fields = ['id', 'ai_generated_at']
