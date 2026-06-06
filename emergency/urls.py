from django.urls import path
from . import views

urlpatterns = [
    path('info/', views.EmergencyInfoView.as_view(), name='emergency-info'),
]
