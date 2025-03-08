from django.db.models import Q
from django.contrib.auth import login, logout
from django.http import JsonResponse
from django_ratelimit.decorators import ratelimit
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet

from barbers.models import Reservation, Barber
from barbers.serializers import ReservationSerializer, BarberSerializer
from users.mixins import RateLimitMixin
from users.models import User, Location
from users.serializers import UserSerializer, LoginSerializer, LocationSerializer
from utilities.jwt_auth import set_tokens_in_cookie



"""
 deleting the given cookies from response.
"""
def delete_cookies(*args, response):
    for arg in args:
        response.delete_cookie(arg)
    return response

"""
Registration View, for all users such as simple users and barbers.
    !!! This View is rate limited !!!
"""
@ratelimit(key='ip', rate='3/m', method='POST', block=True)
@api_view(['POST'])
@permission_classes([AllowAny])
def signup_view(request):
    serializer = UserSerializer(data=request.data, context={'request': request})
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    serializer.save()
    return Response('Registered Successfully!', status=status.HTTP_201_CREATED)



"""
Login View, for all users such as simple users and barbers.
    !!! This View is rate limited !!!
"""
@ratelimit(key='ip', rate='5/m', method='POST', block=True)
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.filter(phone_number=serializer.validated_data['phone_number']).first()
    if not user:
        return Response('User not found', status=status.HTTP_404_NOT_FOUND)
    if not user.check_password(serializer.validated_data['password']):
        return Response('Wrong password!', status=status.HTTP_401_UNAUTHORIZED)
    login(request, user)
    response = set_tokens_in_cookie(user)
    response.status_code = status.HTTP_200_OK
    response.data = UserSerializer(user).data
    return response




"""
Logout View, this view will delete important cookies for more security.
"""
@api_view(['POST'])
@permission_classes([AllowAny])
def logout_view(request):
    logout(request)
    response = Response('Logged out successfully!', status=status.HTTP_200_OK)
    response = delete_cookies('access', 'refresh', 'csrftoken', response=response)
    return response



"""
Refresh View, refreshing access-token by refresh-token for Extending access.
"""
@api_view(['GET'])
@permission_classes([AllowAny])
def refresh(request):
    refresh_token = request.COOKIES.get('refresh')
    if not refresh_token:
        return Response('Refresh token not found!', status=status.HTTP_401_UNAUTHORIZED)
    try:
        refresh = RefreshToken(refresh_token)
        user = User.objects.filter(id=refresh['user_id'], phone_number=refresh['phone_number']).first()
        if not user:
            return Response('Invalid refresh token!', status=status.HTTP_401_UNAUTHORIZED)
        response = Response('Token refreshed!', status=status.HTTP_200_OK)
        response.set_cookie(key='access', value=str(refresh.access_token), httponly=True,
                            secure=True, samesite='None')
        return response
    except Exception:
        return Response('Invalid or Expired refresh token!', status=status.HTTP_401_UNAUTHORIZED)




"""
To change, access, and delete user panel information,
 except location, it has a unique view.
"""
class UserDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    model = User

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        response = self.destroy(request, *args, **kwargs)
        response = delete_cookies('access', 'refresh', 'csrftoken', response=response)
        return response


"""
for set, and change User location.
"""
@permission_classes([IsAuthenticated])
@api_view(['POST', 'PUT'])
def location_view(request):
    location, created = Location.objects.get_or_create(user=request.user)
    if created:
        return Response('location created!', status=status.HTTP_201_CREATED)
    serializer = LocationSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    serializer.update(location, serializer.validated_data)
    return Response(serializer.data, status=status.HTTP_200_OK)


"""
View for users to book an appointment.
Users Cannot set the status and it can only be edited by the barber.
    !!! This View is rate limited !!!
"""
class ReservationViewSet(RateLimitMixin, ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ReservationSerializer
    rate = '3/m'

    def get_queryset(self):
        return Reservation.objects.filter(user_id=self.request.user.pk)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


"""
Custom Error to show to User after rate limit.
"""
def custom_ratelimit_view(request, exception=None):
    return JsonResponse({'Error' : 'Too many requests. you have to wait for a while.'}, status=status.HTTP_429_TOO_MANY_REQUESTS)


"""
This view filters barbers by location in query parameters,
if location is not given, it will filter by default to barbers near the user.
< for example, http:127.0.0.1:8000/users/filter-barbers/?province=KHR, 
            this will filter all barbers in khorasan razavi.
or http:127.0.0.1:8000/users/filter-barbers/?city=mashhad,zone=6,
        this will filter all barbers in the sixth zone of mashhad. >
"""
class BarbersFilterView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        province = request.GET.get('province')
        city = request.GET.get('city')
        zone = request.GET.get('zone')
        filters = Q()

        location = Location.objects.filter(user_id=request.user.pk).first()

        if not province and not city and not zone:
            filters &= Q(location=location)
        if province:
            filters &= Q(location__province=province)
        if city:
            filters &= Q(location__city=city)
        if zone:
            filters &= Q(location__zone=zone)

        barbers = User.objects.filter(filters).filter(barber__isnull=False)
        serializer = UserSerializer(barbers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)





