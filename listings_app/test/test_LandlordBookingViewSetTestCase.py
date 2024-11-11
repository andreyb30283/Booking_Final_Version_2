from datetime import date, timedelta
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from listings_app.models import Booking, Listing, Profile
from listings_app.serializers.serializers import LandlordBookingSerializer


class LandlordBookingViewSetTestCase(APITestCase):
    def setUp(self):
        # Create users
        self.landlord = User.objects.create_user(username="landlord", password="landlordpass")
        self.other_user = User.objects.create_user(username="otheruser", password="otheruserpass")

        # Set up profiles for landlord and other user
        Profile.objects.create(user=self.landlord, is_landlord=True)
        Profile.objects.create(user=self.other_user, is_landlord=False)

        # Create a listing owned by the landlord
        self.listing = Listing.objects.create(
            owner=self.landlord,
            title="Test Listing",
            description="A test listing",
            location="Test Location",
            city="Test City",
            rooms=2,
            property_type="apartment",
            price=1200.00,
            slug="test-listing",

            available_from=date(2024, 11, 10),
            available_until=date(2024, 11, 30),
        )

        # Create initial booking for testing overlapping dates
        self.existing_booking = Booking.objects.create(
            listing=self.listing,
            user=self.other_user,
            start_date=date.today() + timedelta(days=1),
            end_date=date.today() + timedelta(days=10),
            is_confirmed=True
        )

        # Set up URL for the booking view
        self.url = reverse("landlord-bookings-list", kwargs={"listing_slug": self.listing.slug})

        # Set up APIClient and authenticate as landlord
        self.client = APIClient()
        self.client.force_authenticate(user=self.landlord)

    def test_create_booking_success(self):
        # Test successful booking creation without overlapping
        new_booking_data = {
            "listing": self.listing.slug,
            "start_date": date.today() + timedelta(days=11),
            "end_date": date.today() + timedelta(days=15)
        }
        response = self.client.post(self.url, new_booking_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("cancel_deadline", response.data)

    def test_create_booking_overlap(self):
        # Test booking creation with overlapping dates
        overlapping_data = {
            "listing": self.listing.slug,
            "start_date": date.today() + timedelta(days=5),
            "end_date": date.today() + timedelta(days=12)
        }
        response = self.client.post(self.url, overlapping_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "This listing is already booked for the selected dates.")

    def test_delete_booking_not_allowed(self):
        # Test DELETE method should not be allowed
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get_queryset_filter_by_listing_and_owner(self):
        # Verify that only bookings for the landlord's listing are retrieved
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        bookings = response.data
        for booking in bookings:
            self.assertEqual(booking["listing"], self.listing.slug)
            self.assertEqual(Booking.objects.get(id=booking["id"]).listing.owner, self.landlord)
