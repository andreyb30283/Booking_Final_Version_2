from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

from listings_app.models.profile import Profile


class IsLandlord(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            return Profile.objects.get(user=request.user).is_landlord
        except Profile.DoesNotExist:
            return False


class IsNotLandlord(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            if Profile.objects.get(user=request.user).is_landlord:
                return False
            else:
                return True
        except Profile.DoesNotExist:
            return False


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user  # Make sure this matches the correct field in the Booking model


class IsNotOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner != request.user


class IsNotLandlordForCreate(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == 'POST':
            return not getattr(request.user, 'is_landlord', False)
        return True
