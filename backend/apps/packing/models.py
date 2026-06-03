from django.db import models
from django.contrib.auth.models import User
from itinerary.models import Itinerary

class PackingList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='packing_lists')
    itinerary = models.OneToOneField(Itinerary, on_delete=models.CASCADE, related_name='packing_list')
    weather_items = models.JSONField(default=list, blank=True)
    destination_items = models.JSONField(default=list, blank=True)
    medical_items = models.JSONField(default=list, blank=True)
    travel_documents = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Packing list for {self.itinerary.destination}"
