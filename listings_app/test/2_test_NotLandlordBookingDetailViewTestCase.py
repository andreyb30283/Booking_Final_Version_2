from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from listings_app.models import Booking, Listing, Profile
from datetime import date


class NotLandlordBookingDetailViewTestCase(APITestCase):
    def setUp(self):
        # Create users
        self.tenant = User.objects.create_user(username="tenant", password="tenantpass")
        self.landlord = User.objects.create_user(username="landlord", password="landlordpass")
        Profile.objects.create(user=self.tenant, is_landlord=False)
        Profile.objects.create(user=self.landlord, is_landlord=True)
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

        # Create a booking for the tenant
        self.booking = Booking.objects.create(
            listing=self.listing,
            user=self.tenant,
            start_date=date(2024, 11, 10),
            end_date=date(2024, 11, 20),
            is_confirmed=True
        )

        # Endpoint URL for booking detail
        self.url = reverse("booking-detail",
                           kwargs={"listing_slug": self.listing.slug, "pk": self.booking.pk})

        # APIClient setup
        self.tenant_client = APIClient()
        self.landlord_client = APIClient()


    def test_retrieve_booking_as_tenant(self):
        # Authenticate tenant and retrieve their booking
        self.tenant_client.force_authenticate(user=self.tenant)
        response = self.tenant_client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_booking_as_tenant(self):
        # Authenticate tenant and update their booking
        self.tenant_client.force_authenticate(user=self.tenant)
        print(self.tenant)
        updated_data = {"start_date": date(2024, 11, 15),
                        "end_date": date(2024, 11, 25),
                        "listing": "test-listing"
                        }

        response = self.tenant_client.patch(self.url, updated_data, format="json")
        print("Error details:", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_booking_as_landlord(self):
        # Authenticate landlord and attempt to update tenant’s booking
        self.landlord_client.force_authenticate(user=self.landlord)
        updated_data = {"start_date": date(2024, 11, 15), "end_date": date(2024, 11, 25)}
        response = self.landlord_client.patch(self.url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_booking_as_tenant(self):
        # Authenticate tenant and delete their booking
        self.tenant_client.force_authenticate(user=self.tenant)
        response = self.tenant_client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_booking_as_landlord(self):
        # Authenticate landlord and attempt to delete tenant’s booking
        self.landlord_client.force_authenticate(user=self.landlord)
        response = self.landlord_client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_access(self):
        # Unauthenticated access should be forbidden
        client = APIClient()  # Unauthenticated client
        response = client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
