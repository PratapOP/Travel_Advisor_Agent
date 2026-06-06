from django.db import models

class PackingList(models.Model):
    """Packing list associated with a trip itinerary."""
    
    itinerary = models.ForeignKey(
        'itinerary.Itinerary',
        on_delete=models.CASCADE,
        related_name='packing_lists'
    )
    climate_type = models.CharField(max_length=100, blank=True, default='')
    trip_purpose = models.CharField(max_length=100, blank=True, default='leisure')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'packing_lists'
        ordering = ['-created_at']

    def __str__(self):
        return f"Packing List for {self.itinerary.title}"


class PackingItem(models.Model):
    """Individual item within a packing list."""
    
    CATEGORY_CHOICES = [
        ('clothing', 'Clothing'),
        ('toiletries', 'Toiletries & Personal Care'),
        ('electronics', 'Electronics & Gadgets'),
        ('documents', 'Documents & Money'),
        ('health', 'Health & Medical'),
        ('misc', 'Miscellaneous'),
    ]

    packing_list = models.ForeignKey(
        PackingList,
        on_delete=models.CASCADE,
        related_name='items'
    )
    name = models.CharField(max_length=150)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='misc')
    quantity = models.PositiveIntegerField(default=1)
    is_packed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=10, 
        choices=[('high', 'Essential'), ('medium', 'Normal'), ('low', 'Optional')], 
        default='medium'
    )

    class Meta:
        db_table = 'packing_items'
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.name} x{self.quantity} ({'Packed' if self.is_packed else 'Unpacked'})"
