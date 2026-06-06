from django.urls import path
from . import views

urlpatterns = [
    path('info/', views.TourismInfoView.as_view(), name='tourism-info'),
]
