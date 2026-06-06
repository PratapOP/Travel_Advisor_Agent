from rest_framework import generics, permissions
from .models import PackingList, PackingItem
from .serializers import PackingListSerializer, PackingListDetailSerializer, PackingItemSerializer

class PackingListListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PackingListSerializer
        return PackingListDetailSerializer

    def get_queryset(self):
        return PackingList.objects.filter(itinerary__user=self.request.user)

    def perform_create(self, serializer):
        itinerary = serializer.validated_data['itinerary']
        if itinerary.user != self.request.user:
            raise PermissionError("You do not own this itinerary.")
        serializer.save()


class PackingListDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PackingListDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PackingList.objects.filter(itinerary__user=self.request.user)


class PackingItemListView(generics.ListCreateAPIView):
    serializer_class = PackingItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PackingItem.objects.filter(packing_list__itinerary__user=self.request.user)

    def perform_create(self, serializer):
        packing_list = serializer.validated_data['packing_list']
        if packing_list.itinerary.user != self.request.user:
            raise PermissionError("You do not own this packing list.")
        serializer.save()


class PackingItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PackingItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PackingItem.objects.filter(packing_list__itinerary__user=self.request.user)
