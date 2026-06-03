from django.db import models
from itinerary.models import Itinerary

class MedicalGuidance(models.Model):
    itinerary = models.OneToOneField(Itinerary, on_delete=models.CASCADE, related_name='medical_guidance')
    questionnaire_responses = models.JSONField(default=dict, blank=True)
    vaccinations = models.JSONField(default=list, blank=True)
    medicines = models.JSONField(default=list, blank=True)
    precautions = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Medical Guidance for Trip to {self.itinerary.destination}"
