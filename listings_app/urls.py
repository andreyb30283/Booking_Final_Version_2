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
from django.urls import path, re_path

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
# Swagger UI: http://127.0.0.1:8000/api/schema/swagger-ui/
# Redoc UI: http://127.0.0.1:8000/api/schema/redoc/

schema_view = get_schema_view(
    openapi.Info(
        title="Your API Title",
        default_version='v1',
        description="API documentation",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(AllowAny,),
)


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
    # re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    # path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]

from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.views.generic import TemplateView


#
# urlpatterns += [
#     # ...
#     # Route TemplateView to serve the ReDoc template.
#     #   * Provide `extra_context` with view name of `SchemaView`.
#     path(
#         "redoc/",
#         TemplateView.as_view(
#             template_name="redoc.html", extra_context={"schema_url": "openapi-schema"}
#         ),
#         name="redoc",
#     ),
# ]


urlpatterns += [
    # OpenAPI schema endpoint
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    # Swagger UI
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # Redoc UI
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]