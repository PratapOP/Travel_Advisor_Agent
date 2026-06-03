from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Hotel, UserHotel
from .serializers import HotelSerializer, UserHotelSerializer

class HotelListCreateView(generics.ListCreateAPIView):
    serializer_class = HotelSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Hotel.objects.all()
        city = self.request.query_params.get('city')
        country = self.request.query_params.get('country')
        if city:
            queryset = queryset.filter(city__icontains=city)
        if country:
            queryset = queryset.filter(country__icontains=country)
        return queryset

class UserHotelListCreateView(generics.ListCreateAPIView):
    serializer_class = UserHotelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserHotel.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Prevent duplicates
        hotel = serializer.validated_data['hotel']
        if UserHotel.objects.filter(user=self.request.user, hotel=hotel).exists():
            return
        serializer.save(user=self.request.user)

class UserHotelUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserHotelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserHotel.objects.filter(user=self.request.user)

class HotelRecommendView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        city = request.query_params.get('city', '')
        
        # Safe access to profile
        profile = getattr(request.user, 'profile', None)
        budget_pref = profile.budget_preference.lower() if profile else 'moderate'
        
        queryset = Hotel.objects.all()
        if city:
            queryset = queryset.filter(city__icontains=city)
            
        # Segment by price range matches
        if 'budget' in budget_pref:
            queryset = queryset.filter(price_per_night__lt=100.00).order_by('-rating')
        elif 'luxury' in budget_pref:
            queryset = queryset.filter(price_per_night__gte=250.00).order_by('-rating')
        else: # Moderate/Adventure
            queryset = queryset.filter(price_per_night__gte=100.00, price_per_night__lt=250.00).order_by('-rating')
            
        if not queryset.exists():
            queryset = Hotel.objects.filter(city__icontains=city) if city else Hotel.objects.all()
            
        serializer = HotelSerializer(queryset[:5], many=True)
        return Response(serializer.data)

class HotelEmailEnquiryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, hotel_id):
        try:
            hotel = Hotel.objects.get(pk=hotel_id)
        except Hotel.DoesNotExist:
            return Response({"error": "Hotel not found"}, status=status.HTTP_404_NOT_FOUND)
            
        check_in = request.query_params.get('check_in', 'YYYY-MM-DD')
        check_out = request.query_params.get('check_out', 'YYYY-MM-DD')
        guests = request.query_params.get('guests', '1')
        
        username = request.user.first_name or request.user.username
        full_name = request.user.get_full_name() or request.user.username
        
        email_body = f"Subject: Reservation Enquiry - {username}\n\n" \
                     f"Dear {hotel.hotel_name} Reservation Team,\n\n" \
                     f"I hope this email finds you well.\n\n" \
                     f"I would like to enquire about room availability and rates for a stay at your hotel. Here are my trip details:\n\n" \
                     f"- Guest Name: {full_name}\n" \
                     f"- Check-in Date: {check_in}\n" \
                     f"- Check-out Date: {check_out}\n" \
                     f"- Number of Guests: {guests}\n" \
                     f"- Preference: Standard room with generic amenities.\n\n" \
                     f"Could you please confirm if you have availability for these dates and provide details on your best rates? Also, please let me know if breakfast is included in the pricing.\n\n" \
                     f"Thank you for your time, and I look forward to hearing from you.\n\n" \
                     f"Best regards,\n" \
                     f"{full_name}\n" \
                     f"Contact: {request.user.email}\n"

        return Response({
            "hotel_name": hotel.hotel_name,
            "contact_email": hotel.contact_email,
            "email_subject": f"Reservation Enquiry - {username}",
            "email_body": email_body
        })
