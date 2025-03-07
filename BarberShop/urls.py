from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls), # Admin Panel
    path('users/', include('users.urls')),  # Users App URLs
    path('barbers/', include('barbers.urls')), # Barbers App URLs
]

# The Server only serves media such as Pictures in debug mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)