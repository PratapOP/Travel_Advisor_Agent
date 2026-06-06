from rest_framework import views, status, permissions
from rest_framework.response import Response
from .models import EmergencyInfo
from .serializers import EmergencyInfoSerializer
from ai_engine.tools import get_emergency_info

class EmergencyInfoView(views.APIView):
    """Retrieve emergency information for a specific destination. Generates via AI if not cached."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        destination = request.query_params.get('destination')
        if not destination:
            return Response(
                {"error": "Query parameter 'destination' is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        info = EmergencyInfo.objects.filter(destination__iexact=destination.strip()).first()
        if info:
            serializer = EmergencyInfoSerializer(info)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        try:
            ai_data = get_emergency_info.invoke({"destination": destination})
            info = EmergencyInfo.objects.create(
                destination=destination,
                safety_tips=ai_data
            )
            serializer = EmergencyInfoSerializer(info)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": f"Failed to get emergency info: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
