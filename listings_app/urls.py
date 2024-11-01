# from django.urls import path, include
from django.contrib.auth.forms import UserCreationForm
from django.urls import path, reverse_lazy
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views.booking import BookingListCreateView, BookingRetrieveUpdateDestroyView
from .views.listing import ListingListCreateView, ListingRetrieveUpdateDestroyView
from .views.login_logout import LoginView, LogoutView
from .views.review import ReviewListview, ReviewCreateView
from .views.register import RegisterView

#
# router = DefaultRouter()
# router.register(r'profiles', ProfileRetrieveUpdateDestroyView, basename='profile')


urlpatterns = [
    # path('api/register/', RegisterUserView.as_view(), name='register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),


    # path('api/register/', RegisterView.as_view(form_class=UserCreationForm
    #                                            , success_url=reverse_lazy('login')), name='register'),

    path('api/logout/', LogoutView.as_view(), name='logout'),

    # path('api/', include(router.urls)),  # Добавляем маршруты из роутера
    path(r'listings/', ListingListCreateView.as_view(), name='listing-list-create'),
    path(r'listings/<int:pk>/', ListingRetrieveUpdateDestroyView.as_view(), name='listing-detail'),
    path(r'bookings/', BookingListCreateView.as_view(), name='booking-list-create'),
    path(r'bookings/<int:pk>/', BookingRetrieveUpdateDestroyView.as_view(), name='booking-detail'),
    path(r'reviews/', ReviewListview.as_view(), name='review-list'),
    path(r'reviews/create/', ReviewCreateView.as_view(), name='review-create'),
]

# from django.urls import path, include
# from rest_framework import routers
# from . import views
# from .views_api import *
#
# router = routers.DefaultRouter()
# router.register(r'api/profile/',
#                 ProfileRetrieveUpdateDestroyView, basename='yourmodel')
#
# urlpatterns = [
#     path('api/', include(router.urls)),
# ]
#
# urlpatterns = [
#     path('register/', views.register, name='register'),
# ]
#
# from django.contrib.auth import views as auth_views
#
# urlpatterns += [
#     path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
#     path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
# ]
#
# from .views import *
#
# urlpatterns += [
#     # path('api/profile/', ProfileRetrieveUpdateDestroyView.as_view(), name='profile-update'),
#     # Страница редактирования профиля
#     path('/profile/<int:user_id>/', ProfileDetailView.as_view(),
#          name='profile-detail'), ]  # Страница просмотра профиля

#
# from django.urls import path, re_path
# from django.views.decorators.cache import cache_page
#
# from .views import *
#
#
#
#
#
# urlpatterns = [
#     # path('', WomenHome.as_view(), name='home'),
#     # path('about/', about, name='about'),
#     # path('addpage/', AddPage.as_view(), name='add_page'),
#     # path('contact/', ContactFormView.as_view(), name='contact'),
#     path('login/', LoginUser.as_view(), name='login'),
#     path('logout/', logout_user, name='logout'),
#     path('register/', RegisterUser.as_view(), name='register'),
#     # path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
#     # path('category/<slug:cat_slug>/', WomenCategory.as_view(), name='category'),
#
#
# ]
'''
        re_path(r'^archive/(?P<year>[0-9]{4})/', archive)
'''

''' path('path/<int: ...>' , function)  число
    path('path/<slug: ...>' , function) латиница таблицы ASCII ,' - _'
    path('path/<str: ...>', function)  любая строка исключая "/"
    path('path/<uuid: ...>', function) цифры , малые латинские символы ASCII, '-'
    path('path/<path: ...>', function) латинские символы + "/"    
'''
