from django.urls import path
from .views import EmergencyContactSearchView

urlpatterns = [
    path('search/', EmergencyContactSearchView.as_view(), name='emergency_search'),
]
