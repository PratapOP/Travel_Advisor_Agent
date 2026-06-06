from rest_framework import serializers

from .models import HotelPreference, HotelRecommendation


class HotelRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelRecommendation
        fields = [
            'id', 'itinerary', 'name', 'location', 'star_rating',
            'price_per_night', 'currency', 'amenities', 'description',
            'booking_url', 'ai_notes', 'is_booked', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class HotelPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelPreference
        fields = [
            'preferred_star_rating', 'min_budget', 'max_budget',
            'currency', 'must_have_amenities', 'preferred_location_type',
        ]
