from django.contrib.auth import login, logout
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from users.serializers import UserSerializer, LoginSerializer
from utilities.jwt_auth import set_tokens_in_cookie


# Registration view
class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# Login view
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.filter(username=request.data['username']).first()
        if not user:
            return Response({'error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)
        if not user.check_password(request.data['password']):
            return Response({'error': 'Incorrect password'}, status=status.HTTP_401_UNAUTHORIZED)
        login(request, user)
        response = set_tokens_in_cookie(user)
        response.status_code = status.HTTP_201_CREATED
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
        response.data = {'status': 'success'}
        return response


# Just for Testing tokens in development fuzz
class TestView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Refresh Access token
class RefreshTokenView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        refresh_token = request.COOKIES.get('refresh')
        if not refresh_token:
            return Response({'detail': 'Refresh token not found!'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            refresh = RefreshToken(refresh_token)
            user = User.objects.get(id=refresh['user_id'])
            if not user:
                return Response({'detail': 'Invalid refresh token!'}, status=status.HTTP_401_UNAUTHORIZED)
            response = Response({'detail': 'Token refreshed!'}, status=status.HTTP_200_OK)
            response.set_cookie(
                key='access',
                value=str(refresh.access_token),
                httponly=False,
                secure=True,
                samesite='None'
            )
            return response
        except Exception:
            return Response({'detail': 'Invalid or Expired refresh token!'}, status=status.HTTP_401_UNAUTHORIZED)


# GET,PUT,DELETE current user
class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(instance=request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        serializer = UserSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.update(instance=request.user, validated_data=serializer.validated_data)
        return Response({'detail': 'Data Changed Successfully!'}, status=status.HTTP_202_ACCEPTED)

    def delete(self, request):
        try:
            User.objects.filter(username=request.user.username).delete()
        except User.DoesNotExist:
            return Response({'detail': 'User not found!'}, status=status.HTTP_400_BAD_REQUEST)
        response = Response({'detail': 'Account Deleted Successfully!'}, status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie('access')
        response.delete_cookie('refresh')
        response.delete_cookie('csrftoken')
        return response
