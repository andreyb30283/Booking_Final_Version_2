from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView
from listings_app.models.listing import Listing
from listings_app.serializers.serializers import ListingSerializer, SearchQuerySerializer


class SearchListingListView(ListAPIView):
    permission_classes = []
    serializer_class = ListingSerializer
    queryset = Listing.objects.filter(is_active=True)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['price', 'location', 'rooms', 'property_type']
    search_fields = ['title', 'description']
    ordering_fields = ['-price', '-created_at', '-avg_rating']

    def get_queryset(self):
       #/?min_price=100&max_price=1500&city=Ber&rooms_min=2&rooms_max=4&property_type=apartment
        queryset = super().get_queryset()
        title = self.request.query_params.get('title')
        description = self.request.query_params.get('description')
        location = self.request.query_params.get('location')
        city = self.request.query_params.get('city')
        rooms_min = self.request.query_params.get('rooms_min')
        rooms_max = self.request.query_params.get('rooms_max')
        property_type = self.request.query_params.get('property_type')
        price_min = self.request.query_params.get('price_min')
        price_max = self.request.query_params.get('price_max')

        if price_min is not None:
            queryset = queryset.filter(price__gte=price_min)
        if price_max is not None:
            queryset = queryset.filter(price__lte=price_max)
        if location:
            queryset = queryset.filter(location__icontains=location)
        if city:
            queryset = queryset.filter(city__icontains=city)
        if description:
            queryset = queryset.filter(description__icontains=description)
        if title:
            queryset = queryset.filter(title__icontains=title)
        if rooms_min is not None:
            queryset = queryset.filter(rooms__gte=rooms_min)
        if rooms_max is not None:
            queryset = queryset.filter(rooms__lte=rooms_max)
        if property_type:
            queryset = queryset.filter(property_type=property_type)

        if any([title, description, location, city, rooms_min, rooms_max, property_type, price_min, price_max]):
            search_query_data = {
                'owner': self.request.user if self.request.user.is_authenticated else None,
                'title': title,
                'description': description,
                'location': location,
                'city': city,
                'rooms_min': rooms_min,
                'rooms_max': rooms_max,
                'property_type': property_type,
                'price_min': price_min,
                'price_max': price_max,

            }
            # for k in search_query_data:
            #     print(f'{k}!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            # Сохраняем данные запроса
            search_query_serializer = SearchQuerySerializer(data=search_query_data, context={'request':self.request})

            if search_query_serializer.is_valid():
                search_query_serializer.save()
            else:
                print(search_query_serializer.errors)

        return queryset.annotate(avg_rating=Avg('reviews__rating'))

    # def get_serializer_context(self):
    #     # Получаем стандартный контекст
    #     context = super().get_serializer_context()
    #     print(context)
    #     # Добавляем дополнительные данные в контекст
    #     # context['request'] = self.request
    #     return context