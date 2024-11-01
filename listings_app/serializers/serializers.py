from rest_framework import serializers
from listings_app.models import *
from django.contrib.auth.models import User

from listings_app.models.bookings import Booking
from listings_app.models.listings import Listing
from listings_app.models.profiles import Profile
from listings_app.models.reviews import Review

from rest_framework import serializers
from django.contrib.auth.models import User

from django.contrib.auth.models import User
from rest_framework import serializers


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
