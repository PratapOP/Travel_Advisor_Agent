from rest_framework import generics, permissions

from .models import HotelPreference, HotelRecommendation
from .serializers import HotelPreferenceSerializer, HotelRecommendationSerializer


class HotelRecommendationListCreateView(generics.ListCreateAPIView):
    serializer_class = HotelRecommendationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = HotelRecommendation.objects.filter(user=self.request.user)
        itinerary_id = self.request.query_params.get('itinerary')
        if itinerary_id:
            qs = qs.filter(itinerary_id=itinerary_id)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HotelRecommendationDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HotelRecommendationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return HotelRecommendation.objects.filter(user=self.request.user)


class HotelPreferenceView(generics.RetrieveUpdateAPIView):
    serializer_class = HotelPreferenceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj, _ = HotelPreference.objects.get_or_create(user=self.request.user)
        return obj
