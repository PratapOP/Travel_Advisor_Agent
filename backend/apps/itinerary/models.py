from django.db import models
from django.contrib.auth.models import User

class Itinerary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='itineraries')
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    num_days = models.IntegerField()
    budget_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    # Note: wait, it should be max_digits=10, decimal_places=2, decimal_length doesn't exist, it is decimal_places!
    # Let me correct that to max_digits=10, decimal_places=2
    interests = models.CharField(max_length=255, blank=True)
    travel_style = models.CharField(max_length=100, blank=True)
    day_wise_plan = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.source} to {self.destination} ({self.num_days} days)"
