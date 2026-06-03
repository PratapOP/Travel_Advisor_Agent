from django.db import models
from django.contrib.auth.models import User

class Hotel(models.Model):
    hotel_id = models.AutoField(primary_key=True)
    hotel_name = models.CharField(max_length=255)
    city = models.CharField(max_length=100, db_index=True)
    country = models.CharField(max_length=100, db_index=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    contact_email = models.EmailField(max_length=255)
    contact_number = models.CharField(max_length=50)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return f"{self.hotel_name} ({self.city}, {self.country})"

class UserHotel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_hotels')
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='saved_by_users')
    is_compared = models.BooleanField(default=False)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'hotel')

    def __str__(self):
        return f"{self.user.username} - {self.hotel.hotel_name}"
