# listings/views.py
from django.utils import timezone
from rest_framework import generics, permissions, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer

from .serializers import *

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .models.profiles import Profile
from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            # Используем exp для установки времени истечения куки
            access_expiry = datetime.utcfromtimestamp(access_token['exp'])
            refresh_expiry = datetime.utcfromtimestamp(refresh['exp'])
            response = Response(status=status.HTTP_200_OK)
            response.set_cookie(
                key='access_token',
                value=str(access_token),
                httponly=True,
                secure=False,  # Используйте True для HTTPS
                samesite='Lax',
                expires=access_expiry)
            response.set_cookie(
                key='refresh_token',
                value=str(refresh),
                httponly=True,
                secure=False,
                samesite='Lax',
                expires=refresh_expiry
            )
            return response
        else:
            return Response({"detail": "Invalid credentials"},
                            status=status.HTTP_401_UNAUTHORIZED)


#
# class RegisterUserView(APIView):
#     permission_classes = []
#     def post(self, request):
#         username = request.data.get("username")
#         email = request.data.get("email")
#         password = request.data.get("password")
#         phone_number = request.data.get("phone_number")
#         address = request.data.get("address")
#
#         if User.objects.filter(email=email).exists():
#             return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)
#
#         user = User.objects.create_user(username=username, email=email, password=password)
#         Profile.objects.create(user=user, phone_number=phone_number, address=address)
#
#         refresh = RefreshToken.for_user(user)
#         return Response({
#             "user": UserSerializer(user).data,
#             "refresh": str(refresh),
#             "access": str(refresh.access_token),
#         }, status=status.HTTP_201_CREATED)

class ListingListCreateView(generics.ListCreateAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [IsAuthenticated]

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


'''__________________________________________________________________________BOOKING______________________________________________'''


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


'''___________________________________________________________________REVIEW_____________________________________________________________'''


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


'''________________________________________________________________________________________________________________________'''


class ProfileRetrieveUpdateDestroyView(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    pagination_class = [IsAuthenticated]

    # renderer_classes = [JSONRenderer]
    def get_object(self):
        obj = get_object_or_404(Profile, user=self.request.user)
        return obj

#
#
#
#
#
# from django.contrib.auth import logout, login
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from django.contrib.auth.views import LoginView
# from django.http import HttpResponse, HttpResponseNotFound , Http404
# from django.shortcuts import render
# from django.urls import reverse_lazy
# from django.views.generic import CreateView
#
# from .forms import RegisterUserForm
#
#
# from django.shortcuts import redirect
#
# from .forms import *
# from .models import *
# from .utils import *
# '''
# def pageNotFound(request, exception):
#     return HttpResponseNotFound('Site not found')
#
# def index(request):
#     return HttpResponse('Home page')
#
# def archive(request, year):
#     if int(year) > 2020:
#         raise Http404()
#     return HttpResponse(f"<h1> Archive by year</h1><p>{year}</p>")
#
# def categories(request, catid):
#     if request.GET:
#         print(request.GET)
#     return HttpResponse(f"<h1> Article by categories</h1><p>{catid}</p>")
#
#
#
#                                     django.shortcuts.redirect   # status 301 , 302
#
# from django.shortcuts import redirect
#
# def archive(request, year):
#     if int(year) > 2020:
#         return redirect("home" , permanent=True)
#     return HttpResponse(f"<h1> Archive by year</h1><p>{year}</p>")
#
# from django.db import connection
# connection.queries
#
# '''
# def pageNotFound(request, exception):
#     return HttpResponseNotFound('Site not found')
#
#
# # Create your views here.
#
#
# class RegisterUser(DataMixin, CreateView):
#     form_class = RegisterUserForm
#     template_name = 'user/register.html'
#     success_url = reverse_lazy('login')
#
#     def get_context_data(self,*,object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         c_def = self.get_user_context(title='Регистриация')
#         return dict(list(context.items()) + list(c_def.items()))
#
#     def form_valid(self, form):
#         user = form.save()
#         login(self.request, user)
#         return redirect('home')
#
#
# class LoginUser(DataMixin, LoginView):
#     form_class = AuthenticationForm
#     template_name = 'templates/real_estate/login.html'
#
#     def get_context_data(self,*,object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         c_def = self.get_user_context(title='Authorization')
#         return dict(list(context.items()) + list(c_def.items()))
#
#     def get_success_url(self):
#         return reverse_lazy('')
#
# def logout_user(request):
#     logout(request)
#     return redirect('login')
