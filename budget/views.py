from rest_framework import generics, permissions
from .models import BudgetEstimate, Expense
from .serializers import BudgetEstimateSerializer, ExpenseSerializer

class BudgetEstimateListCreateView(generics.ListCreateAPIView):
    serializer_class = BudgetEstimateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = BudgetEstimate.objects.filter(user=self.request.user)
        itinerary_id = self.request.query_params.get('itinerary')
        if itinerary_id:
            qs = qs.filter(itinerary_id=itinerary_id)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BudgetEstimateDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BudgetEstimateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BudgetEstimate.objects.filter(user=self.request.user)


class ExpenseListCreateView(generics.ListCreateAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filter expenses for itineraries owned by this user
        return Expense.objects.filter(itinerary__user=self.request.user)

    def perform_create(self, serializer):
        # The serializer contains itinerary; check if user owns that itinerary in serializer validation or view
        itinerary = serializer.validated_data['itinerary']
        if itinerary.user != self.request.user:
            raise PermissionError("You do not own this itinerary.")
        serializer.save()


class ExpenseDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(itinerary__user=self.request.user)
