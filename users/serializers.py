from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import TravelPreference, User


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True, label='Confirm Password')

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password2',
            'first_name', 'last_name', 'phone', 'nationality',
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Passwords do not match."}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        # Create default travel preferences
        TravelPreference.objects.create(user=user)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile read/update."""

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'phone', 'date_of_birth', 'profile_picture',
            'nationality', 'passport_country', 'bio',
            'date_joined', 'last_login',
        ]
        read_only_fields = ['id', 'username', 'date_joined', 'last_login']


class TravelPreferenceSerializer(serializers.ModelSerializer):
    """Serializer for travel preferences."""

    class Meta:
        model = TravelPreference
        fields = [
            'preferred_budget_tier', 'interests', 'dietary_restrictions',
            'mobility_needs', 'preferred_accommodation', 'travel_style',
            'preferred_climate', 'languages_spoken',
        ]
