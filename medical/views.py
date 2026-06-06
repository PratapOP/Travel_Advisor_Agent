from rest_framework import views, generics, status, permissions
from rest_framework.response import Response
from .models import MedicalInfo, UserMedicalProfile
from .serializers import MedicalInfoSerializer, UserMedicalProfileSerializer
from ai_engine.tools import get_medical_info

class MedicalInfoView(views.APIView):
    """Retrieve medical info for a specific destination. Generates via AI if not cached."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        destination = request.query_params.get('destination')
        if not destination:
            return Response(
                {"error": "Query parameter 'destination' is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        info = MedicalInfo.objects.filter(destination__iexact=destination.strip()).first()
        if info:
            serializer = MedicalInfoSerializer(info)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        try:
            # Get traveler health context if exists
            health_info = ""
            try:
                med_profile = request.user.medical_profile
                conditions = med_profile.medical_conditions
                allergies = ", ".join(med_profile.allergies) if med_profile.allergies else ""
                health_info = f"Conditions: {conditions}. Allergies: {allergies}."
            except Exception:
                pass

            ai_data = get_medical_info.invoke({
                "destination": destination,
                "health_info": health_info
            })
            info = MedicalInfo.objects.create(
                destination=destination,
                advisory_notes=ai_data
            )
            serializer = MedicalInfoSerializer(info)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": f"Failed to get medical info: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserMedicalProfileView(generics.RetrieveUpdateAPIView):
    """Retrieve or update the medical profile of the authenticated user."""
    serializer_class = UserMedicalProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj, _ = UserMedicalProfile.objects.get_or_create(user=self.request.user)
        return obj
