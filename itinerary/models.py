from django.conf import settings
from django.db import models


class Itinerary(models.Model):
    """A travel itinerary plan."""

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('planned', 'Planned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='itineraries',
    )
    title = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    num_travelers = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    ai_generated = models.BooleanField(default=False)
    notes = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'itineraries'
        ordering = ['-created_at']
        verbose_name_plural = 'Itineraries'

    def __str__(self):
        return f"{self.title} — {self.destination}"

    @property
    def num_days(self):
        return (self.end_date - self.start_date).days + 1


class DayPlan(models.Model):
    """A single day within an itinerary."""

    itinerary = models.ForeignKey(
        Itinerary,
        on_delete=models.CASCADE,
        related_name='day_plans',
    )
    day_number = models.PositiveIntegerField()
    date = models.DateField()
    title = models.CharField(max_length=255, blank=True, default='')
    summary = models.TextField(blank=True, default='')

    class Meta:
        db_table = 'day_plans'
        ordering = ['day_number']
        unique_together = ['itinerary', 'day_number']

    def __str__(self):
        return f"Day {self.day_number}: {self.title or self.date}"


class Activity(models.Model):
    """An activity or event within a day plan."""

    CATEGORY_CHOICES = [
        ('sightseeing', 'Sightseeing'),
        ('food', 'Food & Dining'),
        ('adventure', 'Adventure'),
        ('culture', 'Culture'),
        ('shopping', 'Shopping'),
        ('relaxation', 'Relaxation'),
        ('transport', 'Transportation'),
        ('other', 'Other'),
    ]

    day_plan = models.ForeignKey(
        DayPlan,
        on_delete=models.CASCADE,
        related_name='activities',
    )
    time_slot = models.TimeField(null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    location = models.CharField(max_length=255, blank=True, default='')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    estimated_cost = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    currency = models.CharField(max_length=3, default='USD')
    duration_minutes = models.PositiveIntegerField(null=True, blank=True)
    notes = models.TextField(blank=True, default='')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'activities'
        ordering = ['order', 'time_slot']

    def __str__(self):
        return self.title
