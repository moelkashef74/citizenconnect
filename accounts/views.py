from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import UserRegisterSerializer, LoginSerializer,SetNewPasswordSerializer,PasswordResetRequestSerializer, AdminLoginSerializer, VerifyOTPSerializer, UserUpdateSerializer, ChangePasswordSerializer
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework import status
from django.utils.encoding import smart_str
from django.utils.http import urlsafe_base64_decode
from .models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from knox.auth import  TokenAuthentication
from django.contrib.auth import authenticate, login
import vonage
from random import randint
from rest_framework import generics
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from rest_framework.generics import DestroyAPIView



# from .utils import send_code_to_user
# from accounts.models import OneTimePassword
# Create your views here.



class RegisterUserView(GenericAPIView):
    serializer_class=UserRegisterSerializer

    def post(self, request):
        user_data=request.data
        serializer=self.serializer_class(data=user_data)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                user=serializer.data

                # generate OTP
                otp = randint(100000, 999999)

                # store OTP in cache
                cache.set(user['phone'], otp, 300)  # OTP expires after 300 seconds (5 minutes)

                # send OTP via SMS
                client = vonage.Client(key="61ed90e4", secret="zOKWwmXD2VkcrveK")
                sms = vonage.Sms(client)

                responseData = sms.send_message(
                    {
                        "from": "Vonage APIs",
                        "to": user['phone'],
                        "text":f"ahoy  {user['get_full_name']} Your OTP is: {otp}",
                    }
                )

                if responseData["messages"][0]["status"] == "0":
                    print("Message sent successfully.")
                else:
                    print(f"Message failed with error: {responseData['messages'][0]['error-text']}")

                return Response({
                    'data':user,
                    'message':f'Hi, thanks for signing up. We have sent an OTP to your phone number for verification.'
                }, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({'error': 'The number is already exists'}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTPView(GenericAPIView):
    serializer_class = VerifyOTPSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            phone = serializer.validated_data['phone']
            otp = serializer.validated_data['otp']

            # get OTP from cache
            stored_otp = cache.get(phone)

            if stored_otp is not None and stored_otp == otp:
                user = User.objects.get(phone=phone)
                user.is_verified = True
                user.save()
                return Response({'message': 'Phone number verified successfully.'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class LoginUserView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            # Perform login actions
            validated_data = serializer.validated_data
            user = validated_data['user']

            # Check if the user is verified
            if not user.is_verified:
                return Response({'message': 'Your phone number is not verified.'}, status=status.HTTP_400_BAD_REQUEST)

            token = validated_data['token']
            full_name = validated_data['full_name']
            
            # You can perform additional actions here if needed
            
            return Response({
                'full_name': full_name,
                'phone': user.phone,
                'token': token,
                # Include additional fields as needed
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TestAuthView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self, request):
        return Response({'message':'you are authenticated'}, status=status.HTTP_200_OK)
    


class PasswordResetRequestView(GenericAPIView):
    serializer_class=PasswordResetRequestSerializer

    def post(self, request):
        serializer=self.serializer_class(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        return Response({'message':'we have sent you a link to reset your password'}, status=status.HTTP_200_OK)
        # return Response({'message':'user with that email does not exist'}, status=status.HTTP_400_BAD_REQUEST)
    



class PasswordResetConfirm(GenericAPIView):

    def get(self, request, email, token):
        try:
            email = smart_str(urlsafe_base64_decode(email))
            user = User.objects.get(email=email)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'message': 'token is invalid or has expired'}, status=status.HTTP_401_UNAUTHORIZED)
            return Response({'success': True, 'message': 'credentials is valid', 'email': email, 'token': token},
                            status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError as identifier:
            return Response({'message': 'token is invalid or has expired'}, status=status.HTTP_401_UNAUTHORIZED)
class SetNewPasswordView(GenericAPIView):
    serializer_class=SetNewPasswordSerializer

    def patch(self, request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success':True, 'message':"password reset is succesful"}, status=status.HTTP_200_OK)

class LogoutUserView(APIView):
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        # This assumes you have passed the token in the Authorization header
        request._auth.delete()
        return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)

 
class AdminLoginAPIView(APIView):
    def post(self, request):
        serializer = AdminLoginSerializer(data=request.data)
        if serializer.is_valid():
            admin = serializer.validated_data
            print("Admin authenticated:", admin.username)
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        print("Authentication failed:", serializer.errors)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class UserUpdateView(generics.UpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            request.user.set_password(serializer.validated_data['new_password'])
            request.user.save()
            return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteAccountView(DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

