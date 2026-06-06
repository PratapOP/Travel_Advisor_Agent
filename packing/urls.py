from django.urls import path
from . import views

urlpatterns = [
    path('lists/', views.PackingListListCreateView.as_view(), name='packing-list-list'),
    path('lists/<int:pk>/', views.PackingListDetailView.as_view(), name='packing-list-detail'),
    path('items/', views.PackingItemListView.as_view(), name='packing-item-list'),
    path('items/<int:pk>/', views.PackingItemDetailView.as_view(), name='packing-item-detail'),
]
