from rest_framework import viewsets

from listings_app.models import Listing
from listings_app.permissions import IsLandlord, IsOwner
from listings_app.serializers.serializers import LandlordListingSerializer


class LandlordListingViewSet(viewsets.ModelViewSet):
    serializer_class = LandlordListingSerializer
    permission_classes = [IsLandlord, IsOwner]
    lookup_field = 'slug'

    def get_queryset(self):
        return Listing.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
