from django.shortcuts import get_object_or_404
from rest_framework import viewsets


from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from listings_app.models import Booking, Listing
from listings_app.permissions import IsNotLandlord, IsOwner
from listings_app.serializers.serializers import NotLandlordBookingSerializer


# class NotLandlordBookingDetailView(RetrieveUpdateDestroyAPIView):
#     """
#     A view that provides `retrieve`, `update`, and `destroy` actions for a specific booking.
#     """
#     serializer_class = NotLandlordBookingSerializer
#     permission_classes = [IsAuthenticated, IsNotLandlord, IsOwner]
#
#     def get_queryset(self):
#         """
#         Filter bookings by listing slug and user to ensure that only the booking owner
#         can retrieve, update, or delete their booking for a specific listing.
#         """
#         listing_slug = self.kwargs.get("listing_slug")
#         return Booking.objects.filter(listing__slug=listing_slug, owner=self.request.user)
#
#     def perform_update(self, serializer):
#
#         booking = self.get_object()
#         if self.request.user != booking.owner:
#             raise PermissionDenied("You do not have permission to edit this booking.")
#         serializer.save()


class SearchBookingViewSet(viewsets.ModelViewSet):
    serializer_class = NotLandlordBookingSerializer
    permission_classes = [IsAuthenticated, IsNotLandlord]


    def get_queryset(self):
        listing_slug = self.kwargs.get("listing_slug")
        return Booking.objects.filter(listing__slug=listing_slug, owner=self.request.user)

    def perform_create(self, serializer):
        # Retrieve the listing by slug; return a 404 if it doesn't exist
        listing_slug = self.kwargs.get("listing_slug")
        listing = get_object_or_404(Listing, slug=listing_slug)

        # Save the booking with the current user as the owner and associate it with the listing
        serializer.save(owner=self.request.user, listing=listing)
