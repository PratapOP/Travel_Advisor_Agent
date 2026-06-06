from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model with travel-related profile fields."""

    phone = models.CharField(max_length=20, blank=True, default='')
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    nationality = models.CharField(max_length=100, blank=True, default='')
    passport_country = models.CharField(max_length=100, blank=True, default='')
    bio = models.TextField(blank=True, default='')

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username


class TravelPreference(models.Model):
    """User's travel preferences used to personalize AI recommendations."""

    BUDGET_TIERS = [
        ('budget', 'Budget'),
        ('mid_range', 'Mid-Range'),
        ('luxury', 'Luxury'),
        ('ultra_luxury', 'Ultra Luxury'),
    ]

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='travel_preferences'
    )
    preferred_budget_tier = models.CharField(
        max_length=20, choices=BUDGET_TIERS, default='mid_range'
    )
    interests = models.JSONField(
        default=list, blank=True,
        help_text='List of interests e.g. ["adventure", "culture", "food", "nature"]'
    )
    dietary_restrictions = models.JSONField(
        default=list, blank=True,
        help_text='e.g. ["vegetarian", "gluten-free"]'
    )
    mobility_needs = models.TextField(
        blank=True, default='',
        help_text='Any accessibility or mobility requirements'
    )
    preferred_accommodation = models.CharField(max_length=50, blank=True, default='hotel')
    travel_style = models.CharField(
        max_length=50, blank=True, default='balanced',
        help_text='e.g. relaxed, adventurous, cultural, party'
    )
    preferred_climate = models.CharField(max_length=50, blank=True, default='')
    languages_spoken = models.JSONField(default=list, blank=True)

    class Meta:
        db_table = 'travel_preferences'

    def __str__(self):
        return f"{self.user.username}'s preferences"
