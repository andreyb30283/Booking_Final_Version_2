from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from listings_app.models.bookings import Booking
from listings_app.serializers.serializers import BookingSerializer


class BookingListCreateView(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permissions_class = [IsAuthenticated]

    # renderer_classes = [JSONRenderer]
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BookingRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permissions_class = [IsAuthenticated]

    # renderer_classes = [JSONRenderer]
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)
