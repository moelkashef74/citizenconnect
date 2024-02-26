from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from django.utils.encoding import smart_str, force_str, smart_bytes

from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from django.contrib.auth.tokens import PasswordResetTokenGenerator

from django.contrib.sites.shortcuts import get_current_site

from django.urls import reverse

from .utils import send_normal_email
from rest_framework_simplejwt.tokens import RefreshToken, TokenError






class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    password2 = serializers.CharField(max_length=68, min_length=6, write_only=True)
    email_or_phone = serializers.CharField(max_length=255)

    class Meta:
        model = User 
        fields = ['first_name', 'last_name', 'email_or_phone', 'id', 'password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password', '')
        password2 = attrs.get('password2', '')
        if password != password2:
            raise serializers.ValidationError("Passwords do not match")
        return attrs

    def create(self, validated_data):
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        email_or_phone = validated_data.get('email_or_phone')
        id = validated_data.get('id')
        password = validated_data.get('password')

        # Determine if email or phone number
        if '@' in email_or_phone:
            email = email_or_phone
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email_or_phone=email,
                id=id,
                password=password
            )
        else:
            phone_number = email_or_phone
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email_or_phone=phone_number,
                id=id,
                password=password
            )

        return user



class LoginSerializer(serializers.ModelSerializer):
    email_or_phone = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=68, write_only=True)
    full_name = serializers.CharField(max_length=255, read_only=True)
    access_token = serializers.CharField(max_length=255, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['email_or_phone', 'password', 'full_name', 'access_token', 'refresh_token']

    def validate(self, attrs):
        email_or_phone = attrs.get('email_or_phone')
        password = attrs.get('password')
        request = self.context.get('request')

        # Determine if email or phone number
        if '@' in email_or_phone:
            email = email_or_phone
            user = authenticate(request, email=email, password=password)
        else:
            phone_number = email_or_phone
            user = authenticate(request, phone_number=phone_number, password=password)

        if not user:
            raise AuthenticationFailed("Invalid credentials, please try again")

        tokens = user.tokens()
        return {
            'email_or_phone': email_or_phone,
            'full_name': user.get_full_name(),
            'access_token': str(tokens.get('access')),
            'refresh_token': str(tokens.get('refresh'))
        }



class PasswordResetRequestSerializer(serializers.Serializer):
    email_or_phone = serializers.CharField(max_length=255)

    class Meta:
        fields = ['email_or_phone']

    def validate(self, attrs):
        email_or_phone = attrs.get('email_or_phone')
        request = self.context.get('request')

        # Determine if email or phone number
        if '@' in email_or_phone:
            email = email_or_phone
            if User.objects.filter(email_or_phone=email).exists():
                user = User.objects.get(email_or_phone=email)
            else:
                raise serializers.ValidationError("User with this email does not exist")
        else:
            phone_number = email_or_phone
            if User.objects.filter(email_or_phone=phone_number).exists():
                user = User.objects.get(email_or_phone=phone_number)
            else:
                raise serializers.ValidationError("User with this phone number does not exist")

        uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user)
        current_site = get_current_site(request).domain
        relative_link = reverse('reset-password-confirm', kwargs={'uidb64': uidb64, 'token': token})
        abslink = f"http://{current_site}{relative_link}"
        email_body = f"Hi {user.first_name}, use the link below to reset your password: {abslink}"
        data = {
            'email_body': email_body,
            'email_subject': "Reset your Password",
            'to_email': user.email_or_phone
        }
        send_normal_email(data)

        return super().validate(attrs)

    
    
class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=100, min_length=6, write_only=True)
    confirm_password = serializers.CharField(max_length=100, min_length=6, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)
    token = serializers.CharField(min_length=3, write_only=True)

    class Meta:
        fields = ['password', 'confirm_password', 'uidb64', 'token']

    def validate(self, attrs):
        try:
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')
            password = attrs.get('password')
            confirm_password = attrs.get('confirm_password')

            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)
            if password != confirm_password:
                raise serializers.ValidationError({"password": "Passwords do not match"})
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed("Reset link is invalid or has expired", 401)
            
            user.set_password(password)
            user.save()
            return user
        except Exception as e:
            raise AuthenticationFailed("Passwords do not match")


class LogoutUserSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    default_error_messages = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs.get('refresh_token')
        return attrs

    def save(self, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist()
        except TokenError:
            self.fail('bad_token')