from django.urls import path
from .views import TripBudgetDetailView, TripBudgetUpdateView

urlpatterns = [
    path('itinerary/<int:itinerary_id>/', TripBudgetDetailView.as_view(), name='budget_detail'),
    path('<int:pk>/', TripBudgetUpdateView.as_view(), name='budget_update'),
]
