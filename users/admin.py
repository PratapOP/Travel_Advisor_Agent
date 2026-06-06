from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import TravelPreference, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'nationality', 'is_staff']
    list_filter = ['is_staff', 'is_active', 'nationality']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Travel Profile', {
            'fields': ('phone', 'date_of_birth', 'profile_picture', 'nationality', 'passport_country', 'bio'),
        }),
    )


@admin.register(TravelPreference)
class TravelPreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'preferred_budget_tier', 'travel_style', 'preferred_accommodation']
    list_filter = ['preferred_budget_tier', 'travel_style']
