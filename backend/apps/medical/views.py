from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import MedicalGuidance
from .serializers import MedicalGuidanceSerializer

class MedicalGuidanceDetailView(generics.RetrieveAPIView):
    serializer_class = MedicalGuidanceSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'itinerary_id'

    def get_queryset(self):
        return MedicalGuidance.objects.filter(itinerary__user=self.request.user)

class MedicalGuidanceUpdateView(generics.UpdateAPIView):
    serializer_class = MedicalGuidanceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return MedicalGuidance.objects.filter(itinerary__user=self.request.user)

    def perform_update(self, serializer):
        responses = self.request.data.get('questionnaire_responses', {})
        
        # Base recommendations
        vaccines = ["Hepatitis A & B", "Tetanus booster", "Typhoid"]
        medicines = ["Paracetamol", "Antihistamine", "Rehydration salts", "Imodium"]
        precautions = ["Review local weather forecasts before departing."]
        
        # Questionnaire intelligence
        chronic = responses.get('chronic_conditions', '').lower()
        fitness = responses.get('fitness_level', '').lower()
        allergies = responses.get('allergies', '').lower()
        
        if 'asthma' in chronic:
            medicines.append("Asthma Rescue Inhaler")
            precautions.append("Keep your inhaler accessible; notify travel companions of your condition.")
        if 'diabet' in chronic:
            medicines.append("Insulin & monitoring kits")
            precautions.append("Monitor blood sugar regularly during travel; carry fast-acting sugar sources.")
            
        if fitness == 'low':
            precautions.append("Plan extra rest periods; avoid high-intensity hikes.")
        elif fitness == 'high':
            precautions.append("Maintain high hydration and electrolyte levels during strenuous segments.")
            
        if allergies == 'yes' or allergies == 'true':
            medicines.append("EpiPen (Epinephrine) / Antihistamines")
            precautions.append("Carry an allergy card translated to local languages if possible.")
            
        itinerary = serializer.instance.itinerary
        precautions.append(f"Always stay hydrated while exploring {itinerary.destination}.")
        
        serializer.save(
            questionnaire_responses=responses,
            vaccinations=vaccines,
            medicines=medicines,
            precautions=precautions
        )
