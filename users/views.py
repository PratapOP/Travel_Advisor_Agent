from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .models import TravelPreference
from .serializers import (
    TravelPreferenceSerializer,
    UserProfileSerializer,
    UserRegistrationSerializer,
)


class RegisterView(generics.CreateAPIView):
    """User registration endpoint."""

    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "message": "User registered successfully.",
                "user": UserProfileSerializer(user).data,
            },
            status=status.HTTP_201_CREATED,
        )


class ProfileView(generics.RetrieveUpdateAPIView):
    """Retrieve or update the authenticated user's profile."""

    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class TravelPreferenceView(generics.RetrieveUpdateAPIView):
    """Retrieve or update the authenticated user's travel preferences."""

    serializer_class = TravelPreferenceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj, _ = TravelPreference.objects.get_or_create(user=self.request.user)
        return obj
