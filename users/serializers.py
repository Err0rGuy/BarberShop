from rest_framework import serializers
from .models import User, Location
from barbers.models import Barber


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['province', 'city', 'zone']



"""
This serializer only used for Login View
"""
class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField()



class UserSerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True)
    is_barber = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'phone_number', 'password', 'avatar', 'location', 'is_barber']
        extra_kwargs = {
            'id': {'read_only': True},
            'password': {'write_only': True}
        }

    # Check if user is a barber
    def get_is_barber(self, obj):
        return Barber.objects.filter(user=obj).exists()


    """
    Rewritten to hash the password field
    """
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if not password is None:
            instance.set_password(password)
        instance.save()
        is_barber = self.context['request'].data.get('is_barber')
        if is_barber:
            Barber.objects.create(user=instance)
        return instance


    """
    Rewritten to hash the password field,
    and also check if the fields are changed or not.
    this should not be removed or you will get an error. 
    """
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for field in validated_data:
            new_value = validated_data.get(field, None)
            old_value = getattr(instance, field, None)
            if new_value != old_value:
                setattr(instance, field, new_value)
        if not password is None:
            instance.set_password(password)
        instance.save()
        return instance
