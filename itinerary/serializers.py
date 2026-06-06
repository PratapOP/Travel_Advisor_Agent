from rest_framework import serializers

from .models import Activity, DayPlan, Itinerary


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = [
            'id', 'time_slot', 'title', 'description', 'location',
            'category', 'estimated_cost', 'currency', 'duration_minutes',
            'notes', 'order',
        ]


class DayPlanSerializer(serializers.ModelSerializer):
    activities = ActivitySerializer(many=True, read_only=True)

    class Meta:
        model = DayPlan
        fields = ['id', 'day_number', 'date', 'title', 'summary', 'activities']


class ItineraryListSerializer(serializers.ModelSerializer):
    num_days = serializers.ReadOnlyField()

    class Meta:
        model = Itinerary
        fields = [
            'id', 'title', 'destination', 'start_date', 'end_date',
            'num_travelers', 'status', 'ai_generated', 'num_days',
            'created_at', 'updated_at',
        ]


class ItineraryDetailSerializer(serializers.ModelSerializer):
    day_plans = DayPlanSerializer(many=True, read_only=True)
    num_days = serializers.ReadOnlyField()

    class Meta:
        model = Itinerary
        fields = [
            'id', 'title', 'destination', 'start_date', 'end_date',
            'num_travelers', 'status', 'ai_generated', 'notes',
            'num_days', 'day_plans', 'created_at', 'updated_at',
        ]


class ItineraryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Itinerary
        fields = [
            'title', 'destination', 'start_date', 'end_date',
            'num_travelers', 'notes',
        ]

    def validate(self, data):
        if data['end_date'] < data['start_date']:
            raise serializers.ValidationError("End date must be after start date.")
        return data


class AIItineraryRequestSerializer(serializers.Serializer):
    """Input for AI-powered itinerary generation."""
    interests = serializers.CharField(required=False, default='')
    special_requirements = serializers.CharField(required=False, default='')
