from django.urls import path
from .views import MedicalGuidanceDetailView, MedicalGuidanceUpdateView

urlpatterns = [
    path('itinerary/<int:itinerary_id>/', MedicalGuidanceDetailView.as_view(), name='medical_detail'),
    path('<int:pk>/', MedicalGuidanceUpdateView.as_view(), name='medical_update'),
]
