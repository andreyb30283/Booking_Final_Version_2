from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from listings_app.models import Listing, Booking


class SearchBookingViewSetTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client.login(username="testuser", password="password123")

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

        self.booking = Booking.objects.create(
            listing=self.listing,
            user=self.user,
            start_date="2024-11-15",
            end_date="2024-11-20",
            is_confirmed=True
        )

    def test_create_booking(self):
        url = reverse("booking-list", kwargs={"listing_slug": self.listing.slug})
        data = {
            "start_date": "2024-12-01",
            "end_date": "2024-12-05",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)

    def test_update_booking(self):
        url = reverse("booking-detail", kwargs={"listing_slug": self.listing.slug, "pk": self.booking.pk})
        data = {
            "start_date": "2024-12-05",
            "end_date": "2024-12-10",
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, 200)

    def test_unauthorized_booking_cancellation(self):
        another_user = User.objects.create_user(username="otheruser", password="password123")
        self.client.force_authenticate(user=another_user)
        url = reverse("booking-detail", kwargs={"listing_slug": self.listing.slug, "pk": self.booking.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)