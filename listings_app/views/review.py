from django.utils import timezone
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated


from listings_app.models.bookings import Booking
from listings_app.models.listings import Listing
from listings_app.models.reviews import Review
from listings_app.serializers.serializers import ReviewSerializer


class ReviewListview(generics.ListAPIView):
    serializer_class = ReviewSerializer

    # renderer_classes = [JSONRenderer]
    def get_queryset(self):
        listings_id = self.kwargs.get('listing_id')
        return Review.objects.filter(listings_id=listings_id)


class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Listing.objects.all()
    serializer_class = ReviewSerializer
    # renderer_classes = [JSONRenderer]


class ReviewCreateView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]  # Только авторизованные пользователи

    # renderer_classes = [JSONRenderer]
    def perform_create(self, serializer):
        booking_id = self.request.data.get('booking')  # Получаем бронирование из данных запроса
        try:
            booking = Booking.objects.get(id=booking_id, user=self.request.user)
        except Booking.DoesNotExist:
            raise PermissionDenied("You are not allowed to leave a review for this booking.")
        if booking.end_date >= timezone.now().date():  # Проверяем, завершено ли бронирование
            raise PermissionDenied("You cannot leave a review until the booking is completed.")
        if Review.objects.filter(
                booking=booking).exists():  # Проверяем, оставлял ли пользователь отзыв на это бронирование
            raise PermissionDenied("You have already left a review for this booking.")
        serializer.save(user=self.request.user, listing=booking.listing,
                        booking=booking)  # Создаем отзыв, привязанный к бронированию
