from django.contrib.auth.models import User
from django.core.validators import EmailValidator
from rest_framework import serializers
from django.contrib.auth import authenticate
from listings_app.models.profile import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['phone_number', 'is_landlord']


class RegisterSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'password2', 'email', 'first_name', 'last_name', 'profile']
        read_only_fields = ['id']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}
        }

        ref_name = 'CustomUserSerializer'

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords must match.")
        else:
            data.pop('password2')
        return data

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('A user with this email already exists')
        return value

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', {})
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        # Извлекаем данные профиля
        # phone_number = validated_data.pop('phone_number', '')
        # is_landlord = validated_data.pop('is_landlord', False)

        user.set_password(password)
        user.save()
        Profile.objects.create(user=user, phone_number=profile_data.get('phone_number', ''),
                               is_landlord=profile_data.get('is_landlord', False))

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(validators=[EmailValidator()])
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['email'], password=data['password'])
        if user is None:
            raise serializers.ValidationError("Invalid login credentials.")
        return user
