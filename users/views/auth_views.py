from django.contrib.auth import login, logout
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from users.models import User
from users.serializers import UserSerializer, BarberSerializer, LoginSerializer
from utilities.jwt_auth import set_tokens_in_cookie


# Registration view
class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = serializer.save()
        if request.data['is_barber']:
            BarberSerializer(user=user).save()
        return Response('Registered Successfully!', status=status.HTTP_201_CREATED)


# Login view
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.filter(phone_number=request.data['phone_number']).first()
        if not user:
            return Response('User not found', status=status.HTTP_404_NOT_FOUND)
        if not user.check_password(request.data['password']):
            return Response('Wrong password', status=status.HTTP_401_UNAUTHORIZED)
        login(request, user)
        response = set_tokens_in_cookie(user)
        response.status_code = status.HTTP_200_OK
        response.data = UserSerializer(user).data
        return response


# Logout view
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        response = Response()
        response.delete_cookie('access')
        response.delete_cookie('refresh')
        response.status_code = status.HTTP_200_OK
        response.data = 'Logged out successfully!'
        return response


# Just for Testing tokens in development fuzz
class TestView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


# GET,PUT,DELETE current user
# class UserDetailView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request):
#         serializer = UserSerializer(instance=request.user)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def put(self, request):
#         serializer = UserSerializer(data=request.data)
#         try:
#             serializer.is_valid(raise_exception=True)
#         except ValidationError:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         serializer.update(instance=request.user, validated_data=serializer.validated_data)
#         return Response('Data Changed Successfully!', status=status.HTTP_202_ACCEPTED)
#
#     def delete(self, request):
#         try:
#             User.objects.filter(phone_number=request.user.phone_number).delete()
#         except User.DoesNotExist:
#             return Response('User not found!', status=status.HTTP_400_BAD_REQUEST)
#         response = Response('Account Deleted Successfully!', status=status.HTTP_204_NO_CONTENT)
#         response.delete_cookie('access')
#         response.delete_cookie('refresh')
#         response.delete_cookie('csrftoken')
#         return response


class UserDetails(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)
