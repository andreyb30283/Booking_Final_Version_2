# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework_simplejwt.tokens import RefreshToken
# from listings_app.serializers.register_login import RegisterSerializer, LoginSerializer
#
# class RegisterView(APIView):
#     def post(self, request, *args, **kwargs):
#         serializer = RegisterSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             return Response({"message": "User registered successfully"},
#                             status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# class LoginView(APIView):
#     def post(self, request, *args, **kwargs):
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.validated_data
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token),
#             })
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)