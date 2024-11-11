from datetime import timedelta
from rest_framework import viewsets, status
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from listings_app.models import Booking
from listings_app.permissions import IsLandlord
from listings_app.serializers.serializers import LandlordBookingSerializer


class LandlordBookingViewSet(viewsets.ModelViewSet):
    serializer_class = LandlordBookingSerializer
    permission_classes = [IsAuthenticated, IsLandlord]

    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed("DELETE")

    def get_queryset(self):
        # print(self.kwargs)
        # Получаем ID объявления из маршрута и фильтруем бронирования по нему
        listing_slug = self.kwargs.get("listing_slug")  # self.kwargs['listing_pk']
        # print(listing_id,listing_id,listing_id,listing_id,listing_id,)
        return Booking.objects.filter(listing__slug=listing_slug, listing__owner=self.request.user)

    def perform_create(self, serializer):
        listing = serializer.validated_data['listing']
        start_date = serializer.validated_data['start_date']
        end_date = serializer.validated_data['end_date']

        # Проверка доступности объекта на указанные даты
        overlapping_bookings = Booking.objects.filter(
            listing=listing,
            start_date__lt=end_date,
            end_date__gt=start_date,
            is_canceled=False
        )
        if overlapping_bookings.exists():
            return Response(
                {"error": "This listing is already booked for the selected dates."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Устанавливаем крайний срок отмены за 2 дня до начала бронирования
        cancel_deadline = start_date - timedelta(days=2)
        serializer.save(user=self.request.user, cancel_deadline=cancel_deadline)
