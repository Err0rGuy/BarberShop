from rest_framework import serializers

from users.models import User, Barber, UnAvailability, WorkDay, OffTime, Reservation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'phone_number', 'password', 'avatar', 'location')
        extra_kwargs = {
            'id': {'read_only': True},
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if not password is None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for field in validated_data:
            instance.__setattr__(field, validated_data.get(field))
        if not password is None:
            instance.set_password(password)
        instance.save()
        return instance


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ('id', 'user_id', 'barber_id', 'date', 'accept_status')


class UnAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UnAvailability
        fields = ('id', 'start_date', 'end_date', 'reason')


class OffTimesSerializer(serializers.ModelSerializer):
    class Meta:
        model = OffTime
        fields = ('id', 'start_time', 'end_time', 'reason')


class WorkDaysSerializer(serializers.ModelSerializer):
    off_times = OffTimesSerializer(many=True)

    class Meta:
        model = WorkDay
        fields = ('id', 'day', 'start_time', 'end_time', 'off_times')


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)


class BarberSerializer(serializers.ModelSerializer):
    unavailability = UnAvailabilitySerializer(read_only=True, many=True)
    workdays = WorkDaysSerializer(read_only=True, many=True)
    off_times = OffTimesSerializer(read_only=True, many=True)

    class Meta:
        model = Barber
        fields = ('user_id', 'is_available', 'max_reservation_days',
                  'reservation_gap', 'unavailability', 'workdays', 'off_times')
