from rest_framework import serializers
from .models import PackingList, PackingItem

class PackingItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackingItem
        fields = ['id', 'packing_list', 'name', 'category', 'quantity', 'is_packed', 'priority']
        read_only_fields = ['id']


class PackingListDetailSerializer(serializers.ModelSerializer):
    items = PackingItemSerializer(many=True, read_only=True)

    class Meta:
        model = PackingList
        fields = ['id', 'itinerary', 'climate_type', 'trip_purpose', 'items', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class PackingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackingList
        fields = ['id', 'itinerary', 'climate_type', 'trip_purpose', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
