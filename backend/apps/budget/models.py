from django.db import models
from django.contrib.auth.models import User
from itinerary.models import Itinerary

class TripBudget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')
    itinerary = models.OneToOneField(Itinerary, on_delete=models.CASCADE, related_name='budget')
    total_cost = models.DecimalField(max_digits=12, decimal_places=2)
    accommodation_cost = models.DecimalField(max_digits=12, decimal_places=2)
    food_budget = models.DecimalField(max_digits=12, decimal_places=2)
    transport_budget = models.DecimalField(max_digits=12, decimal_places=2)
    emergency_reserve = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Budget for {self.itinerary.destination} - Total: {self.total_cost}"
