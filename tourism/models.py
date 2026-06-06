from django.db import models

class TourismInfo(models.Model):
    """General tourism details for a destination country or city."""
    
    destination = models.CharField(max_length=255, unique=True)
    local_customs = models.TextField(blank=True, default='')
    language_tips = models.TextField(blank=True, default='')
    currency_info = models.TextField(blank=True, default='')
    best_time_to_visit = models.CharField(max_length=150, blank=True, default='')
    safety_rating = models.CharField(max_length=50, blank=True, default='')
    visa_requirements = models.TextField(blank=True, default='')
    ai_generated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tourism_info'
        verbose_name_plural = 'Tourism Info'

    def __str__(self):
        return f"Tourism Info for {self.destination}"


class Attraction(models.Model):
    """Specific landmark, spot or attraction in a destination."""
    
    tourism_info = models.ForeignKey(
        TourismInfo,
        on_delete=models.CASCADE,
        related_name='attractions'
    )
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100, blank=True, default='')
    description = models.TextField(blank=True, default='')
    entry_fee = models.CharField(max_length=100, blank=True, default='Free')
    opening_hours = models.CharField(max_length=255, blank=True, default='')
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)

    class Meta:
        db_table = 'attractions'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.tourism_info.destination})"
