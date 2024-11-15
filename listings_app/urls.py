from django.urls import path, include, re_path
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from listings_app.views.auth.login import LoginView
from listings_app.views.auth.logout import LogoutView
from listings_app.views.auth.profile import ProfileRetrieveUpdateDestroyView
from listings_app.views.auth.register import RegisterView
from listings_app.views.landlord.booking import LandlordBookingViewSet
from listings_app.views.landlord.listings import LandlordListingViewSet
from listings_app.views.search.booking import SearchBookingViewSet
from listings_app.views.search.listing import SearchListingListView
from listings_app.views.search.review import ListingReviewView
from listings_app.views.search_query import SearchQueryListView
from django.urls import path

router = DefaultRouter()
router.register('profiles', ProfileRetrieveUpdateDestroyView, basename='profile')
router.register('landlord-listings', LandlordListingViewSet, basename='landlord-listings')


urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    path('search-listings/', SearchListingListView.as_view(), name='search-listings'),
    path('search-listings/<slug:listing_slug>/reviews/', ListingReviewView.as_view(), name='listing-review'),
    path('search-listings/<slug:listing_slug>/bookings/',
         SearchBookingViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='booking-list-create'),
    path('search-listings/<slug:listing_slug>/bookings/<int:pk>/',
         SearchBookingViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'}),
         name='booking-detail'),


    path('landlord-listings/<slug:listing_slug>/bookings/', LandlordBookingViewSet.as_view({'get': 'list'}),
         name='landlord-booking-list'),
    path('landlord-listings/<slug:listing_slug>/bookings/<int:pk>/',
         LandlordBookingViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update'}),
         name='landlord-booking-detail'),
    path('search-queries/', SearchQueryListView.as_view(), name='search-query-list'),
]
