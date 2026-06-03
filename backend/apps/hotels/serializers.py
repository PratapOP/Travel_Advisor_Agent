from rest_framework import serializers
from .models import Hotel, UserHotel

class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = [
            'hotel_id', 
            'hotel_name', 
            'city', 
            'country', 
            'rating', 
            'price_per_night', 
            'contact_email', 
            'contact_number', 
            'latitude', 
            'longitude'
        ]

class UserHotelSerializer(serializers.ModelSerializer):
    hotel = HotelSerializer(read_only=True)
    hotel_id = serializers.PrimaryKeyRelatedField(
        queryset=Hotel.objects.all(), source='hotel', write_only=True
    )

    class Meta:
        model = UserHotel
        fields = ['id', 'hotel', 'hotel_id', 'is_compared', 'saved_at']
        read_only_fields = ['id', 'saved_at']
