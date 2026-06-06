from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='user-register'),
    path('profile/', views.ProfileView.as_view(), name='user-profile'),
    path('preferences/', views.TravelPreferenceView.as_view(), name='travel-preferences'),
]
