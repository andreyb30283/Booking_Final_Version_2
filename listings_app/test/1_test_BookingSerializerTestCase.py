from rest_framework.test import APIClient, APITestCase
from django.contrib.auth.models import User
from listings_app.models import Booking, Listing
from listings_app.serializers import BookingSerializer
from django.utils import timezone
from datetime import timedelta


class BookingSerializerTestCase(APITestCase):

    def setUp(self):
        # Set up users, listings, and bookings for testing
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.other_user = User.objects.create_user(username="otheruser", password="password123")
        self.listing = Listing.objects.create(
            owner=self.user,
            title="Test Listing",
            description="A nice place to stay",
            location="Berlin",
            city="Berlin",
            rooms=3,
            property_type="apartment",
            price=1000,
            slug="test-listing"
        )

        # Booking created by self.user
        self.booking = Booking.objects.create(
            listing=self.listing,
            user=self.user,
            start_date=timezone.now().date() + timedelta(days=1),
            end_date=timezone.now().date() + timedelta(days=5),
            is_confirmed=True,
            cancel_deadline=timezone.now().date()
        )

        # Booking with past deadline for cancellation test
        self.past_deadline_booking = Booking.objects.create(
            listing=self.listing,
            user=self.user,
            start_date=timezone.now().date() - timedelta(days=10),
            end_date=timezone.now().date() - timedelta(days=5),
            is_confirmed=True,
            cancel_deadline=timezone.now().date() - timedelta(days=7)
        )

    def test_cancel_booking_success(self):
        """Test that the user can successfully cancel a booking before the deadline."""
        serializer = BookingSerializer(
            instance=self.booking,
            data={'is_canceled': True},
            context={'user': self.user}
        )
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.booking.refresh_from_db()
        self.assertTrue(self.booking.is_canceled)
        print("Success: User was able to cancel booking before the deadline.")

    def test_cancel_booking_past_deadline(self):
        """Test that a user cannot cancel a booking after the cancellation deadline."""
        serializer = BookingSerializer(
            instance=self.past_deadline_booking,
            data={'is_canceled': True},
            context={'user': self.user}
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn("Cancellation deadline has passed.", serializer.errors["non_field_errors"])
        print("Success: User could not cancel booking after the deadline.")

    def test_cancel_booking_different_user(self):
        """Test that a different user cannot cancel the booking."""
        serializer = BookingSerializer(
            instance=self.booking,
            data={'is_canceled': True},
            context={'user': self.other_user}  # Different user attempting cancellation
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn("You do not have permission to cancel this booking.", serializer.errors["non_field_errors"])
        print("Success: Different user was prevented from canceling the booking.")