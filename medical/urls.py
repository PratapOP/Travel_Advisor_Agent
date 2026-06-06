from django.urls import path
from . import views

urlpatterns = [
    path('info/', views.MedicalInfoView.as_view(), name='medical-info'),
    path('profile/', views.UserMedicalProfileView.as_view(), name='medical-profile'),
]
