from rest_framework import views, status, permissions
from rest_framework.response import Response
from .models import TourismInfo, Attraction
from .serializers import TourismInfoSerializer
from ai_engine.tools import get_tourism_info

class TourismInfoView(views.APIView):
    """Retrieve tourism info for a specific destination. Generates via AI if not cached."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        destination = request.query_params.get('destination')
        if not destination:
            return Response(
                {"error": "Query parameter 'destination' is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check cache/database first
        info = TourismInfo.objects.filter(destination__iexact=destination.strip()).first()
        if info:
            serializer = TourismInfoSerializer(info)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        # Trigger LangChain tool to fetch destination information
        try:
            ai_data = get_tourism_info.invoke({"destination": destination})
            # Save to DB
            info = TourismInfo.objects.create(
                destination=destination,
                local_customs=ai_data
            )
            serializer = TourismInfoSerializer(info)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": f"Failed to get tourism info: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
