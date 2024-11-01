from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

from .models.bookings import Booking
from .models.listings import Listing
from .models.profiles import Profile
from .models.reviews import Review

from rest_framework import serializers
from django.contrib.auth.models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'password2')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords must match.")
        return data

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = '__all__'


class ListingSerializer(serializers.ModelSerializer):
    owner = ProfileSerializer()

    class Meta:
        model = Listing
        fields = '__all__'
        read_only_fields = ['id', 'owner', 'created_at', 'update_at']


class BookingSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    listing = ListingSerializer()

    class Meta:
        model = Booking
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    listing = ListingSerializer()
    user = UserSerializer()

    class Meta:
        model = Review
        fields = '__all__'
