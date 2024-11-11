from django.contrib import admin

# Register your models here.
from .models.profile import Profile
from django.contrib import admin

#
# @admin.register(Profile)
# class UserProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'is_site_user', 'phone_number')

from .models.booking import Booking
from .models.listing import Listing
from .models.profile import Profile
from .models.review import Review

admin.site.register(Listing)
admin.site.register(Booking)
admin.site.register(Review)
admin.site.register(Profile)
