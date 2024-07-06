from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from django.utils.encoding import smart_str, force_str, smart_bytes

from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import timezone
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.hashers import check_password
from django.urls import reverse
from django.db import IntegrityError
from .utils import send_normal_email
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from .models import Admin
from knox.models import AuthToken






class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    password2 = serializers.CharField(max_length=68, write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'email', 'password', 'password2','get_full_name']

    def validate(self, attrs):
        password = attrs.get('password', '')
        password2 = attrs.get('password2', '')
        if password != password2:
            raise serializers.ValidationError("Passwords do not match")

        phone = attrs.get('phone', '')
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError("A user with this phone number already exists.")
        return attrs

    def create(self, validated_data):
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        phone = validated_data.get('phone')
        email = validated_data.get('email')
        password = validated_data.get('password')


        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            email=email,
            password=password,
            is_verified = True,
        )

        return user

class VerifyOTPSerializer(serializers.Serializer):
    phone = serializers.CharField()
    otp = serializers.IntegerField()




class LoginSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=68, write_only=True)
    full_name = serializers.CharField(max_length=255, read_only=True)
    access_token = serializers.CharField(max_length=255, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['phone', 'password', 'full_name', 'access_token', 'refresh_token']

    def validate(self, attrs):
        phone = attrs.get('phone')
        password = attrs.get('password')
        request = self.context.get('request')

        if phone.startswith('01'):
            # Prepend '+2' to the phone number
            phone = '+2' + phone
        user = authenticate(request, phone=phone, password=password)
        if user:
            # This will create a Knox token and return the token key
            token = AuthToken.objects.create(user)[1]

            return {
                'user': user,
                'phone': phone,
                'full_name': user.get_full_name,
                'token': token
            }
        else:
            raise AuthenticationFailed("Invalid credentials, please try again")



class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        request = self.context.get('request')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
        else:
            raise serializers.ValidationError("User with this email does not exist")

        token = PasswordResetTokenGenerator().make_token(user)
        current_site = get_current_site(request).domain
        relative_link = reverse('reset-password-confirm', kwargs={'email': urlsafe_base64_encode(smart_bytes(user.email)), 'token': token})
        abslink = f"http://{current_site}{relative_link}"
        email_body = f"Hi {user.first_name}, use the link below to reset your password: {abslink}"
        data = {
            'email_body': email_body,
            'email_subject': "Reset your Password",
            'to_email': user.email
        }
        send_normal_email(data)

        return super().validate(attrs)



class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=100, min_length=6, write_only=True)
    confirm_password = serializers.CharField(max_length=100, min_length=6, write_only=True)
    email = serializers.CharField(min_length=1, write_only=True)
    token = serializers.CharField(min_length=3, write_only=True)

    class Meta:
        fields = ['password', 'confirm_password', 'email', 'token']

    def validate(self, attrs):
        try:
            token = attrs.get('token')
            email = attrs.get('email')
            password = attrs.get('password')
            confirm_password = attrs.get('confirm_password')


            user = User.objects.get(email=email)

            if password != confirm_password:
                raise serializers.ValidationError("Passwords do not match")
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError("Reset link is invalid or has expired", code='token_invalid')

            user.set_password(password)
            user.save()
            return user
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError("Link is invalid or has expired")
        

class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    default_error_messages = {
        'bad_token': ('Token is invalid or expired')
    }   

    def validate_refresh_token(self, value):
        self.token = value
        return {'refresh_token': self.token}

    
    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            return self.fail('bad_token')
        

class AdminLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            raise serializers.ValidationError("Username and password are required.")

        admin = Admin.objects.filter(username=username).first()
        if admin and admin.check_password(password):
            return admin
        raise serializers.ValidationError("Incorrect username or password.")



from rest_framework import serializers
from .models import User

class UserUpdateSerializer(serializers.ModelSerializer):

    first_name = serializers.CharField(max_length=255, required=False)
    last_name = serializers.CharField(max_length=255, required=False)
    phone = serializers.CharField(max_length=255, required=False)
    email = serializers.EmailField(required=False)
    photo = serializers.ImageField(required=False)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'email', 'photo']

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.email = validated_data.get('email', instance.email)
        instance.photo = validated_data.get('photo', instance.photo)
        instance.save()
        return instance


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Password fields didn't match."})
        return data

    def validate_current_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError({"current_password": "Current password is not correct"})
        return value