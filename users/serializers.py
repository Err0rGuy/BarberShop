from rest_framework import serializers

from users.models import User, BarberProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'phone_number', 'password', 'has_barber_profile')
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


class BarberProfileSerializer(UserSerializer):
    class Meta:
        model = BarberProfile
        fields = ('personal_image', 'location', 'certification_image', 'user_id')


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)