from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Itinerary
from .serializers import ItinerarySerializer
from ai_engine.agent import generate_itinerary, generate_budget, generate_packing
from budget.models import TripBudget
from packing.models import PackingList
from medical.models import MedicalGuidance

class ItineraryListCreateView(generics.ListCreateAPIView):
    serializer_class = ItinerarySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Itinerary.objects.filter(user=self.request.user).order_by('-created_at')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        source = serializer.validated_data['source']
        destination = serializer.validated_data['destination']
        num_days = serializer.validated_data['num_days']
        budget_amount = serializer.validated_data['budget_amount']
        interests = serializer.validated_data.get('interests', '')
        travel_style = serializer.validated_data.get('travel_style', '')
        
        # Invoke AI generation
        plan_data = generate_itinerary(
            source=source,
            destination=destination,
            num_days=num_days,
            budget_amount=float(budget_amount),
            interests=interests,
            travel_style=travel_style
        )
        
        itinerary = serializer.save(
            user=request.user,
            day_wise_plan=plan_data.get('day_wise_plan', [])
        )
        
        # Auto-create downstream models
        try:
            budget_data = generate_budget(destination, num_days, float(budget_amount), travel_style)
            TripBudget.objects.create(
                user=request.user,
                itinerary=itinerary,
                total_cost=budget_data['total_cost'],
                accommodation_cost=budget_data['accommodation_cost'],
                food_budget=budget_data['food_budget'],
                transport_budget=budget_data['transport_budget'],
                emergency_reserve=budget_data['emergency_reserve']
            )
            
            packing_data = generate_packing(destination, num_days, interests)
            PackingList.objects.create(
                user=request.user,
                itinerary=itinerary,
                weather_items=packing_data['weather_items'],
                destination_items=packing_data['destination_items'],
                medical_items=packing_data['medical_items'],
                travel_documents=packing_data['travel_documents']
            )
            
            # Default medical warnings and vaccine guidelines
            MedicalGuidance.objects.create(
                itinerary=itinerary,
                questionnaire_responses={},
                vaccinations=["Hepatitis A & B", "Tetanus booster", "Typhoid"],
                medicines=["Paracetamol", "Antihistamine", "Rehydration salts", "Imodium"],
                precautions=[
                    f"Stay hydrated in {destination}.",
                    "Carry a copy of prescriptions.",
                    "Review local weather forecasts before departing."
                ]
            )
        except Exception as e:
            # We catch exceptions to prevent rolling back the itinerary if a linked generator fails
            print(f"Error generating downstream trip entities: {e}")
            
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class ItineraryDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = ItinerarySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Itinerary.objects.filter(user=self.request.user)
