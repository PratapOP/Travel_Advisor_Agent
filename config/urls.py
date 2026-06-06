"""
URL configuration for Travel Advisor Agent.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),

    # JWT Authentication
    path('api/v1/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # App URLs
    path('api/v1/auth/', include('users.urls')),
    path('api/v1/chat/', include('chatagent.urls')),
    path('api/v1/itinerary/', include('itinerary.urls')),
    path('api/v1/hotels/', include('hotels.urls')),
    path('api/v1/budget/', include('budget.urls')),
    path('api/v1/packing/', include('packing.urls')),
    path('api/v1/tourism/', include('tourism.urls')),
    path('api/v1/emergency/', include('emergency.urls')),
    path('api/v1/medical/', include('medical.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
