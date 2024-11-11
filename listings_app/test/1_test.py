from unittest import TestCase

from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from listings_app.models import Listing, SearchQuery
from django.contrib.auth.models import User


class ListingListViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='landlord', password='useruser')

        # Создаем тестовые данные для объектов Listing
        self.listing1 = Listing.objects.create(
            title='Cozy Apartment',
            description='A cozy 2-bedroom apartment',
            location='Berlin',
            city='Berlin',
            rooms=2,
            property_type='apartment',
            price=1200.00,
            owner=self.user  # Указываем владельца
        )
        self.listing2 = Listing.objects.create(
            title='Modern House',
            description='A modern 3-bedroom house',
            location='Munich',
            city='Munich',
            rooms=3,
            property_type='house',
            price=2500.00,
            owner=self.user  # Указываем владельца
        )

        # Устанавливаем клиент для тестирования и логиним пользователя
        self.client = APIClient()
        self.client.login(username='landlord', password='useruser')

    def test_get_listing_with_filters(self):
        response = self.client.get(reverse('listings'), {
            'min_price': 1000,
            'max_price': 2000,
            'location': 'Berlin'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Cozy Apartment')

    def test_post_listing_search_query(self):
        post_data = {
            'title': 'Cozy Apartment',
            'description': 'A cozy 2-bedroom apartment',
            'location': 'Berlin',
            'city': 'Berlin',
            'rooms_min': 1,
            'rooms_max': 3,
            'property_type': 'apartment',
            'price_min': 1000,
            'price_max': 1500

        }
        response = self.client.post(reverse('listings'), post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Cozy Apartment')
        self.assertTrue(SearchQuery.objects.filter(user='landlord').exists())

    def test_post_invalid_search_query(self):
        # Тестирование POST-запроса с некорректными данными
        post_data = {
            'title': 'Test',
            'description': 'Invalid data',
            'location': '',
            'city': 'Berlin',
            'rooms_min': 'invalid',  # Некорректное значение
            'property_type': 'invalid_type'  # Некорректный тип
        }
        response = self.client.post(reverse('listings'), post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def tearDown(self):
        self.client.logout()




class ListingModelTest(TestCase):
    def test_create_listing(self):
        listing = Listing.objects.create(
            title="Test Listing",
            description="Test Description",
            price=100,
            location="Test Location"
        )
        self.assertEqual(listing.title, "Test Listing")