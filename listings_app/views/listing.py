from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from listings_app.models.listings import Listing
from listings_app.serializers.serializers import ListingSerializer


class ListingListCreateView(generics.ListCreateAPIView):

    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = []

    # renderer_classes = [JSONRenderer]
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)  # Устанавливаем владельца объявления как текущего пользователя


class ListingRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [IsAuthenticated]  # Доступ к редактированию и удалению только для авторизованных пользователей

    # renderer_classes = [JSONRenderer]
    def get_queryset(self):
        """
        Ограничим доступ к редактированию и удалению только для владельца объявления.
        """
        return Listing.objects.filter(owner=self.request.user)