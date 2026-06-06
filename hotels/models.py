from django.conf import settings
from django.db import models


class HotelRecommendation(models.Model):
    """AI-generated or manually saved hotel recommendation."""

    STAR_CHOICES = [(i, f'{i} Star') for i in range(1, 6)]

    itinerary = models.ForeignKey(
        'itinerary.Itinerary',
        on_delete=models.CASCADE,
        related_name='hotel_recommendations',
        null=True, blank=True,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='hotel_recommendations',
    )
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    star_rating = models.PositiveIntegerField(choices=STAR_CHOICES, null=True, blank=True)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=3, default='USD')
    amenities = models.JSONField(default=list, blank=True)
    description = models.TextField(blank=True, default='')
    booking_url = models.URLField(blank=True, default='')
    ai_notes = models.TextField(blank=True, default='', help_text='AI-generated recommendation notes')
    is_booked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'hotel_recommendations'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.location})"


class HotelPreference(models.Model):
    """User's hotel preferences for AI personalization."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='hotel_preferences',
    )
    preferred_star_rating = models.PositiveIntegerField(default=3)
    min_budget = models.DecimalField(max_digits=10, decimal_places=2, default=50)
    max_budget = models.DecimalField(max_digits=10, decimal_places=2, default=200)
    currency = models.CharField(max_length=3, default='USD')
    must_have_amenities = models.JSONField(
        default=list, blank=True,
        help_text='e.g. ["wifi", "pool", "gym", "breakfast"]',
    )
    preferred_location_type = models.CharField(
        max_length=50, blank=True, default='central',
        help_text='e.g. central, beachfront, quiet suburb',
    )

    class Meta:
        db_table = 'hotel_preferences'

    def __str__(self):
        return f"{self.user.username}'s hotel preferences"
