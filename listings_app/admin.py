from django.contrib import admin

# Register your models here.
from .models.profiles import Profile
from django.contrib import admin

#
# @admin.register(Profile)
# class UserProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'is_site_user', 'phone_number')

from .models.bookings import Booking
from .models.listings import Listing
from .models.profiles import Profile
from .models.reviews import Review

admin.site.register(Listing)
admin.site.register(Booking)
admin.site.register(Review)
admin.site.register(Profile)
