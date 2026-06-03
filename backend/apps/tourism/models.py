from django.db import models

class TouristSpot(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=100, db_index=True)
    country = models.CharField(max_length=100, db_index=True)
    description = models.TextField()
    category = models.CharField(max_length=100, default='Popular Attraction') # e.g. Popular Attraction, Hidden Gem, Local Experience, Photography Location
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.5)
    image_url = models.CharField(max_length=500, blank=True, default='')

    def __str__(self):
        return f"{self.name} ({self.city}, {self.country})"

class PhotoPose(models.Model):
    CATEGORY_CHOICES = (
        ('solo', 'Solo Poses'),
        ('couple', 'Couple Poses'),
        ('family', 'Family Poses'),
        ('adventure', 'Adventure Poses'),
    )
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    image_reference = models.CharField(max_length=500, blank=True, default='')

    def __str__(self):
        return f"{self.get_category_display()} - {self.description[:30]}..."
