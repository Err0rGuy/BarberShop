from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'workdays', WorkDayViewSet, basename='workdays')   # Workdays ViewSet
router.register(r'unavailability', UnAvailabilityViewSet, basename='unavailability')  # Unavailability ViewSet
router.register(r'images', ImageGalleryViewSet, basename='images') # ImageGallery ViewSet
router.register(r'offtimes', OffTimeViewSet, basename='offtimes') # Off times ViewSet

urlpatterns = [
    path('details/', BarberDetailView.as_view(), name='barber-details'),
    path('reservations/', ReservationListView.as_view(), name='reservations_get'),
    path('reservations/<int:pk>/', ReservationDetailView.as_view(), name='reservation'),
    path('', include(router.urls)),
]