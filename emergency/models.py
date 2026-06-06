from django.db import models

class EmergencyInfo(models.Model):
    """Emergency and safety details for a destination country/city."""
    
    destination = models.CharField(max_length=255, unique=True)
    emergency_numbers = models.JSONField(
        default=dict, blank=True,
        help_text='e.g. {"police": "112", "ambulance": "112", "fire": "112"}'
    )
    embassy_info = models.TextField(blank=True, default='')
    safety_tips = models.TextField(blank=True, default='')
    travel_warnings = models.TextField(blank=True, default='')
    ai_generated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'emergency_info'
        verbose_name_plural = 'Emergency Info'

    def __str__(self):
        return f"Emergency Info for {self.destination}"
