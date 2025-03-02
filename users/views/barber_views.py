from django.db.utils import IntegrityError
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import Barber
from users.serializers import BarberSerializer

# Create, modify, delete, or get Barber profile
class ProfilesView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BarberSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.validated_data['user'] = request.user
            serializer.save()
        except ValidationError:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            return Response({'detail' : 'Profile for this user already created!'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        try:
            serializer = BarberSerializer(Barber.objects.get(user_id=request.user.id))
        except Barber.DoesNotExist:
            return Response({'detail' : 'No profile found!'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        serializer = BarberSerializer(data=request.data)
        try:
            profile = Barber.objects.get(user_id=request.user.id)
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Barber.DoesNotExist:
            return Response({'detail' : 'No profile found!'}, status=status.HTTP_404_NOT_FOUND)
        serializer.update(instance=profile, validated_data=serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request):
        try:
            Barber.objects.filter(user_id=request.user.pk).delete()
        except Barber.DoesNotExist:
            return Response({'detail' : 'Profile not found!'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'Profile Deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
