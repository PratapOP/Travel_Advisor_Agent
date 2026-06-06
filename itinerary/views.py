import logging

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from ai_engine.tools import generate_itinerary

from .models import Itinerary
from .serializers import (
    AIItineraryRequestSerializer,
    ItineraryCreateSerializer,
    ItineraryDetailSerializer,
    ItineraryListSerializer,
)

logger = logging.getLogger('ai_engine')


class ItineraryListCreateView(generics.ListCreateAPIView):
    """List all itineraries or create a new one."""

    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ItineraryCreateSerializer
        return ItineraryListSerializer

    def get_queryset(self):
        return Itinerary.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ItineraryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a specific itinerary."""

    serializer_class = ItineraryDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Itinerary.objects.filter(user=self.request.user)


class AIGenerateItineraryView(APIView):
    """Generate an AI-powered itinerary for an existing itinerary."""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            itinerary = Itinerary.objects.get(pk=pk, user=request.user)
        except Itinerary.DoesNotExist:
            return Response(
                {"error": "Itinerary not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = AIItineraryRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get user preferences
        budget_tier = 'mid_range'
        try:
            budget_tier = request.user.travel_preferences.preferred_budget_tier
        except Exception:
            pass

        # Invoke AI tool
        result = generate_itinerary.invoke({
            "destination": itinerary.destination,
            "start_date": str(itinerary.start_date),
            "end_date": str(itinerary.end_date),
            "num_days": itinerary.num_days,
            "num_travelers": itinerary.num_travelers,
            "budget_tier": budget_tier,
            "interests": serializer.validated_data.get('interests', ''),
            "special_requirements": serializer.validated_data.get('special_requirements', ''),
        })

        # Mark itinerary as AI-generated
        itinerary.ai_generated = True
        itinerary.notes = result
        itinerary.save(update_fields=['ai_generated', 'notes'])

        return Response({
            "itinerary_id": itinerary.id,
            "ai_plan": result,
            "message": "AI itinerary generated successfully.",
        })
