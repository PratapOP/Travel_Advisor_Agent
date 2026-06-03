from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import TouristSpot, PhotoPose
from .serializers import TouristSpotSerializer, PhotoPoseSerializer

class TouristSpotListView(generics.ListAPIView):
    serializer_class = TouristSpotSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = TouristSpot.objects.all()
        city = self.request.query_params.get('city')
        country = self.request.query_params.get('country')
        category = self.request.query_params.get('category')
        if city:
            queryset = queryset.filter(city__icontains=city)
        if country:
            queryset = queryset.filter(country__icontains=country)
        if category:
            # Match categories like Popular Attraction, Hidden Gem, Local Experience, Photography Location
            queryset = queryset.filter(category__icontains=category)
        return queryset

class PhotoPoseListView(generics.ListAPIView):
    serializer_class = PhotoPoseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = PhotoPose.objects.all()
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__iexact=category)
        return queryset
