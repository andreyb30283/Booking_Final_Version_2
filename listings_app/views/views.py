# listings/views.py
from django.utils import timezone
from rest_framework import generics, permissions, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer

from listings_app.serializers import *

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from listings_app.models.profiles import Profile
from listings_app.serializers import UserSerializer
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
# class LogoutView(APIView):
#     def post(self, request, *args, **kwargs):
#         response = Response(status=status.HTTP_204_NO_CONTENT)
#         response.delete_cookie('access_token')
#         response.delete_cookie('refresh_token')
#         return response
#
# class LoginView(APIView):
#     permission_classes = [AllowAny]
#
#     def post(self, request, *args, **kwargs):
#         username = request.data.get('username')
#         password = request.data.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user:
#             refresh = RefreshToken.for_user(user)
#             access_token = refresh.access_token
#             # Используем exp для установки времени истечения куки
#             access_expiry = datetime.utcfromtimestamp(access_token['exp'])
#             refresh_expiry = datetime.utcfromtimestamp(refresh['exp'])
#             response = Response(status=status.HTTP_200_OK)
#             response.set_cookie(
#                 key='access_token',
#                 value=str(access_token),
#                 httponly=True,
#                 secure=False,  # Используйте True для HTTPS
#                 samesite='Lax',
#                 expires=access_expiry)
#             response.set_cookie(
#                 key='refresh_token',
#                 value=str(refresh),
#                 httponly=True,
#                 secure=False,
#                 samesite='Lax',
#                 expires=refresh_expiry
#             )
#             return response
#         else:
#             return Response({"detail": "Invalid credentials"},
#                             status=status.HTTP_401_UNAUTHORIZED)


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




'''__________________________________________________________________________BOOKING______________________________________________'''



'''___________________________________________________________________REVIEW_____________________________________________________________'''


'''________________________________________________________________________________________________________________________'''


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
