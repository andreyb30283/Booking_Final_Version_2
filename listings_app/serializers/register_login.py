from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate

from listings_app.models.profiles import Profile


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User  # Теперь модель - это User, так как Profile расширяет User
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords must match.")
        return data

    def create(self, validated_data):
        # Удаляем поле password2, так как оно не нужно для создания User
        validated_data.pop('password2')
        password = validated_data.pop('password')

        # Создаем пользователя
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        # Создаем профиль, связанный с пользователем
        Profile.objects.create(user=user)  # Если у профиля есть обязательные поля, добавьте их здесь

        return user


# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True, required=True)
#     password2 = serializers.CharField(write_only=True, required=True)
#
#     class Meta:
#         model = User
#         fields = ('email', 'username', 'password', 'password2')
#
#     def validate(self, data):
#         if data['password'] != data['password2']:
#             raise serializers.ValidationError("Passwords must match.")
#         return data
#
#     def create(self, validated_data):
#         user = User(
#             email=validated_data['email'],
#             username=validated_data['username']
#         )
#         user.set_password(validated_data['password'])
#         user.save()
#         return user



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['email'], password=data['password'])
        if user is None:
            raise serializers.ValidationError("Invalid login credentials.")
        return user