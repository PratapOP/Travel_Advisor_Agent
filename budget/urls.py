from django.urls import path
from . import views

urlpatterns = [
    path('estimates/', views.BudgetEstimateListCreateView.as_view(), name='budget-estimate-list'),
    path('estimates/<int:pk>/', views.BudgetEstimateDetailView.as_view(), name='budget-estimate-detail'),
    path('expenses/', views.ExpenseListCreateView.as_view(), name='expense-list'),
    path('expenses/<int:pk>/', views.ExpenseDetailView.as_view(), name='expense-detail'),
]
