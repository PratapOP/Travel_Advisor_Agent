from django.urls import path
from .views import PackingListDetailView, PackingListUpdateView

urlpatterns = [
    path('itinerary/<int:itinerary_id>/', PackingListDetailView.as_view(), name='packing_detail'),
    path('<int:pk>/', PackingListUpdateView.as_view(), name='packing_update'),
]
