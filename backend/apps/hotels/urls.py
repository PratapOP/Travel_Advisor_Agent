from django.urls import path
from .views import (
    HotelListCreateView,
    UserHotelListCreateView,
    UserHotelUpdateDeleteView,
    HotelRecommendView,
    HotelEmailEnquiryView
)

urlpatterns = [
    path('', HotelListCreateView.as_view(), name='hotel_list_create'),
    path('saved/', UserHotelListCreateView.as_view(), name='user_hotel_list_create'),
    path('saved/<int:pk>/', UserHotelUpdateDeleteView.as_view(), name='user_hotel_detail'),
    path('recommend/', HotelRecommendView.as_view(), name='hotel_recommend'),
    path('<int:hotel_id>/enquiry/', HotelEmailEnquiryView.as_view(), name='hotel_enquiry'),
]
