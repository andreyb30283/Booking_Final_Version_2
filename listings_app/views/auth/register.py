from datetime import datetime

from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken

from listings_app.models.profile import Profile
from listings_app.serializers.register_login import RegisterSerializer
from listings_app.serializers.serializers import UserSerializer


def set_jwt_cookies(response, user):
    refresh_token = RefreshToken.for_user(user)
    access_token = refresh_token.access_token
    # Устанавливает JWT токены в куки.
    access_expiry = datetime.utcfromtimestamp(access_token['exp'])
    refresh_expiry = datetime.utcfromtimestamp(refresh_token['exp'])
    response.set_cookie(
        key='access_token',
        value=str(access_token),
        httponly=True,
        secure=False,
        samesite='Lax',
        expires=access_expiry
    )
    response.set_cookie(
        key='refresh_token',
        value=str(refresh_token),
        httponly=True,
        secure=False,
        samesite='Lax',
        expires=refresh_expiry
    )


class RegisterView(APIView):
    permission_classes = []
    serializer_class = RegisterSerializer

    class Meta:
        # model = Profile
        fields = '__all__'

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            response = Response(data=serializer.validated_data
                # {
                # 'user': user.id,
                # 'username': user.username,
                # 'email': user.email,
                # 'message': 'User created successfully'
                # }

            , status=status.HTTP_201_CREATED)
            set_jwt_cookies(response, user)
            return response
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    # def get(self, request):
    #     return Response({
    #             'user': {
    #                 'username': 13,
    #                 'email': 12 }})