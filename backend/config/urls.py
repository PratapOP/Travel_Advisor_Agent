from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/itinerary/', include('itinerary.urls')),
    path('api/hotels/', include('hotels.urls')),
    path('api/budget/', include('budget.urls')),
    path('api/packing/', include('packing.urls')),
    path('api/emergency/', include('emergency.urls')),
    path('api/tourism/', include('tourism.urls')),
    path('api/medical/', include('medical.urls')),
    path('api/chat/', include('chatagent.urls')),
    
    # Catch-all to serve index.html for Single Page Application client-side routing
    re_path(r'^.*$', TemplateView.as_view(template_name='index.html'), name='index'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
