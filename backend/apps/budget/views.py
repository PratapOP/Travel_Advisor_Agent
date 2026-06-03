from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import TripBudget
from .serializers import TripBudgetSerializer

class TripBudgetDetailView(generics.RetrieveAPIView):
    serializer_class = TripBudgetSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'itinerary_id'

    def get_queryset(self):
        return TripBudget.objects.filter(user=self.request.user)

class TripBudgetUpdateView(generics.UpdateAPIView):
    serializer_class = TripBudgetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TripBudget.objects.filter(user=self.request.user)
