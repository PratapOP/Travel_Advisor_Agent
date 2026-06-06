from django.db import models
from django.conf import settings

class MedicalInfo(models.Model):
    """Medical advisory and health requirements for a destination country/region."""
    
    destination = models.CharField(max_length=255, unique=True)
    required_vaccinations = models.JSONField(default=list, blank=True)
    recommended_vaccinations = models.JSONField(default=list, blank=True)
    health_risks = models.TextField(blank=True, default='')
    insurance_recommendations = models.TextField(blank=True, default='')
    advisory_notes = models.TextField(blank=True, default='', help_text='AI-generated advisory notes')
    ai_generated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'medical_info'
        verbose_name_plural = 'Medical Info'

    def __str__(self):
        return f"Medical Info for {self.destination}"


class UserMedicalProfile(models.Model):
    """User's sensitive health information stored for emergency/medical reference."""
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='medical_profile'
    )
    allergies = models.JSONField(default=list, blank=True, help_text='List of allergies')
    medications = models.JSONField(default=list, blank=True, help_text='Current medications')
    blood_type = models.CharField(max_length=5, blank=True, default='')
    medical_conditions = models.TextField(blank=True, default='')
    emergency_contact_name = models.CharField(max_length=150, blank=True, default='')
    emergency_contact_phone = models.CharField(max_length=50, blank=True, default='')

    class Meta:
        db_table = 'user_medical_profiles'

    def __str__(self):
        return f"Medical Profile for {self.user.username}"
