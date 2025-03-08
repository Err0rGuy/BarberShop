from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *


router = DefaultRouter()
router.register('reservations', ReservationViewSet, basename='reservations') # Reservations ViewSet
urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('details/', UserDetailView.as_view(), name='details'),
    path('token-refresh/', refresh, name='token_refresh'),
    path('location/', location_view, name='location'),
    path('', include(router.urls)),
]