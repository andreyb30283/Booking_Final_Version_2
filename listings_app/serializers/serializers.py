from django.db.models import Avg
from django.utils import timezone

from listings_app.models import Booking
from listings_app.models.listing import Listing
from listings_app.models.profile import Profile
from listings_app.models.review import Review

from django.contrib.auth.models import User
from rest_framework import serializers

from listings_app.models.search_query import SearchQuery
from listings_app.serializers.review import ReviewSerializer


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", 'password']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ProfileReadOnlySerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = '__all__'


class NotLandlordBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'listing', 'owner', 'start_date', 'end_date', 'is_confirmed', 'is_canceled', 'cancel_deadline']
        read_only_fields = ['listing', 'owner', 'is_confirmed', 'cancel_deadline']

    def update(self, instance, validated_data):
        request = self.context.get('request')
        user = request.user if request else None

        if instance.owner != user:
            raise serializers.ValidationError("You do not have permission to cancel this booking.")

        # Only allow cancellation if the deadline has not passed
        if validated_data.get('is_canceled', False):
            if timezone.now().date() > instance.cancel_deadline:
                raise serializers.ValidationError("The cancellation deadline has passed.")
            instance.is_canceled = True
        else:
            # Allow updating other fields if needed (e.g., dates) here
            instance.start_date = validated_data.get('start_date', instance.start_date)
            instance.end_date = validated_data.get('end_date', instance.end_date)

        instance.save()
        return instance


class LandlordBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['id', 'listing', 'owner', 'start_date', 'end_date', 'is_canceled']


class LandlordListingSerializer(serializers.ModelSerializer):
    bookings = LandlordBookingSerializer(many=True, read_only=True)

    class Meta:
        model = Listing
        fields = '__all__'
        read_only_fields = ['id', 'owner', 'created_at', 'update_at', 'slug']


class ListingSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Listing
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['reviews_count'] = instance.reviews.count()
        avg_rating = instance.reviews.aggregate(Avg('rating')).get('rating__avg')

        representation['avg_rating'] = avg_rating if avg_rating is not None else 0
        return representation


class ReviewReadSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  # Отображаем имя пользователя, оставившего отзыв

    class Meta:
        model = Review
        fields = ['id', 'listing', 'user', 'rating', 'comment', 'created_at', 'updated_at']
        read_only_fields = ['listing', 'user', 'created_at']


class ReviewWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['user', 'rating']


class SearchQuerySerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = SearchQuery
        fields = '__all__'
        read_only_fields = ['owner', 'created_at']
