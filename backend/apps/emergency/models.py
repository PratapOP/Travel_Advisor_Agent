from django.db import models

class EmergencyContact(models.Model):
    emergency_id = models.AutoField(primary_key=True)
    country = models.CharField(max_length=100, db_index=True)
    city = models.CharField(max_length=100, db_index=True)
    police_contact = models.CharField(max_length=50)
    ambulance_contact = models.CharField(max_length=50)
    tourist_helpline = models.CharField(max_length=50)
    embassy_contact = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Emergency Contact - {self.city}, {self.country}"
