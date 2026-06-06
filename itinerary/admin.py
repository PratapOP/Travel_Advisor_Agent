from django.contrib import admin

from .models import Activity, DayPlan, Itinerary


class DayPlanInline(admin.TabularInline):
    model = DayPlan
    extra = 0


class ActivityInline(admin.TabularInline):
    model = Activity
    extra = 0


@admin.register(Itinerary)
class ItineraryAdmin(admin.ModelAdmin):
    list_display = ['title', 'destination', 'user', 'start_date', 'end_date', 'status', 'ai_generated']
    list_filter = ['status', 'ai_generated']
    search_fields = ['title', 'destination']
    inlines = [DayPlanInline]


@admin.register(DayPlan)
class DayPlanAdmin(admin.ModelAdmin):
    list_display = ['itinerary', 'day_number', 'date', 'title']
    inlines = [ActivityInline]
