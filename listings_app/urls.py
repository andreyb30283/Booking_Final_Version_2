from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from listings_app.views.auth.login import LoginView
from listings_app.views.auth.logout import LogoutView
from listings_app.views.auth.profile import ProfileRetrieveUpdateDestroyView
from listings_app.views.auth.register import RegisterView
from listings_app.views.landlord.booking import LandlordBookingViewSet

from listings_app.views.landlord.listings import LandlordListingViewSet
from listings_app.views.search.booking import NotLandlordBookingDetailView, SearchBookingViewSet
from listings_app.views.search.listing import SearchListingListView

from listings_app.views.search.review import ListingReviewView


# Main router
router = DefaultRouter()
router.register('profiles', ProfileRetrieveUpdateDestroyView, basename='profile')

router.register('landlord-listings', LandlordListingViewSet, basename='landlord-listings')


router2 = DefaultRouter()
router2.register(r'bookings', SearchBookingViewSet, basename='search-booking')
urlpatterns = [
    path('api/', include([
        path('', include(router.urls)),
        # path('', include(listings_router.urls)),
        path('landlord-listings/<slug:listing_slug>/bookings/',
             LandlordBookingViewSet.as_view({'get': 'list'}),
             name='landlord-booking-list'),
        path('landlord-listings/<slug:listing_slug>/bookings/<int:pk>/',
             LandlordBookingViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update'}),
             name='landlord-booking-detail'),

        path('auth/', include([
            path('register/', RegisterView.as_view(), name='register'),
            path('login/', LoginView.as_view(), name='login'),
            path('logout/', LogoutView.as_view(), name='logout'),
            path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
            path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        ])),

        path('search-listings/', SearchListingListView.as_view(), name='search-listings'),
        path('search-listings/<slug:listing_slug>/', include([
            path('reviews/', ListingReviewView.as_view(), name='listing-review'),
            path('', include(router2.urls)),
            path('bookings/<int:pk>/', NotLandlordBookingDetailView.as_view(), name='booking-detail'),
        ])),
    ])),
]
