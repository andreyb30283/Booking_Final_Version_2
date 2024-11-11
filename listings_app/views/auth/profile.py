from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from listings_app.models.profile import Profile
from listings_app.serializers.register_login import ProfileSerializer
from listings_app.serializers.serializers import ProfileReadOnlySerializer


class ProfileRetrieveUpdateDestroyView(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    pagination_class = [IsAuthenticated]

    # renderer_classes = [JSONRenderer]
    def get_object(self):
        obj = get_object_or_404(Profile, user=self.request.user)
        return obj

#
# from rest_framework import viewsets
#
# class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
#     '''READ ONLY'''
#     queryset = Profile.objects.all()
#     serializer_class = ProfileReadOnlySerializer
#     permission_classes = [IsAuthenticated]