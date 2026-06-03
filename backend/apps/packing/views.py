from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import PackingList
from .serializers import PackingListSerializer

class PackingListDetailView(generics.RetrieveAPIView):
    serializer_class = PackingListSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'itinerary_id'

    def get_queryset(self):
        return PackingList.objects.filter(user=self.request.user)

class PackingListUpdateView(generics.UpdateAPIView):
    serializer_class = PackingListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PackingList.objects.filter(user=self.request.user)
