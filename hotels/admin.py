from django.contrib import admin

from .models import HotelPreference, HotelRecommendation


@admin.register(HotelRecommendation)
class HotelRecommendationAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'star_rating', 'price_per_night', 'is_booked', 'user']
    list_filter = ['star_rating', 'is_booked']
    search_fields = ['name', 'location']


@admin.register(HotelPreference)
class HotelPreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'preferred_star_rating', 'min_budget', 'max_budget']
