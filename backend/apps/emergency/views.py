from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import EmergencyContact
from .serializers import EmergencyContactSerializer

class EmergencyContactSearchView(generics.ListAPIView):
    serializer_class = EmergencyContactSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = EmergencyContact.objects.all()
        country = self.request.query_params.get('country')
        city = self.request.query_params.get('city')
        if country:
            queryset = queryset.filter(country__icontains=country)
        if city:
            queryset = queryset.filter(city__icontains=city)
        return queryset
