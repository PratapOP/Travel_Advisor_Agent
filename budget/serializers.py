from rest_framework import serializers
from .models import BudgetEstimate, Expense

class BudgetEstimateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetEstimate
        fields = ['id', 'itinerary', 'total_estimated', 'currency', 'breakdown', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'itinerary', 'category', 'amount', 'currency', 'description', 'date', 'created_at']
        read_only_fields = ['id', 'created_at']
