from rest_framework import serializers
from .models import *


class BarberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Barber
        fields = ('id', 'user_id', 'is_available', 'max_reservation_days', 'reservation_gap')
        extra_kwargs = {
            'id': {'read_only': True},
            'user_id': {'read_only': True}
        }


class ReservationSerializer(serializers.ModelSerializer):
    barber = serializers.PrimaryKeyRelatedField(queryset=Barber.objects.all(), required=True)

    def validate(self, data):
        instance = Reservation(**data)
        try:
            instance.clean()
        except ValidationError as e:
            raise serializers.ValidationError(e.detail)
        return data

    class Meta:
        model = Reservation
        fields = ('id', 'user', 'barber', 'date', 'status')
        extra_kwargs = {
            'id': {'read_only': True},
            'user': {'read_only': True},
            'status': {'read_only': True},
        }


"""
This serializer only user for barbers to change reservations status (accepted, ignored, waiting)...
barbers only can change the status.
"""
class BarberReservationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ('status',)
        extra_kwargs = {
            'status': {'required': True},
        }


class UnAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UnAvailability
        fields = ('id', 'start_date', 'end_date', 'reason')
        extra_kwargs = {
            'id': {'read_only': True}
        }

    def validate(self, data):
        instance = UnAvailability(**data)
        try:
            instance.clean()
        except ValidationError as e:
            raise serializers.ValidationError(e.detail)
        return data


class WorkDaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkDay
        fields = ('id', 'day', 'start_time', 'end_time')
        extra_kwargs = {
            'id': {'read_only': True}
        }


class OffTimesSerializer(serializers.ModelSerializer):
    def validate(self, data):
        instance = OffTime(**data)
        try:
            instance.clean()
        except ValidationError as e:
            raise serializers.ValidationError(e.detail)
        return data

    class Meta:
        model = OffTime
        fields = ('id', 'start_time', 'end_time', 'reason', 'workday')
        extra_kwargs = {
            'id': {'read_only': True},
            'workday': {'read_only': True}
        }


class ImageGalleySerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageGallery
        fields = ('id', 'image')
        extra_kwargs = {
            'id': {'read_only': True}
        }
