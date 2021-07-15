from django.contrib.auth import authenticate
from django.http import JsonResponse, Http404
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.urls import reverse

from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

from .serializers import UserRegisterSerializer, UserVerifySerializer, UserLoginSerializer, UserChangePasswordSerializer, UserResetPasswordSerializer, UserResetConfirmPasswordSerializer, UserSerializer
from .models import User
from .utils import EmailSending, generate_key
from .permissions import UserVerifyPermission
import jwt
import pyotp

class UserRegisterView(APIView):

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            # Sending email to verify user
            user_data       = serializer.data
            user            = User.objects.get(email=user_data['email'])
            token           = RefreshToken.for_user(user).access_token
            current_site    = get_current_site(request).domain
            relative_link   = reverse('verify-user')
            absolute_url    = f'http://{current_site+relative_link}?token={str(token)}'
            email_body      = f'Hi {user.email},\n Use the link below to verify your email \n{absolute_url}'
            data            = {
                                'email_body': email_body, 
                                'to_email': user.email,
                                'email_subject': 'Verify your email'
                            }

            EmailSending.send_email(data)

            return JsonResponse({
                'status': 'success',
                'message': 'Register successful!'
            }, status=status.HTTP_201_CREATED)

        return JsonResponse({
            'status': 'error',
            'message': serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)

class UserVerifyView(APIView):
    serializer_class = UserVerifySerializer

    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()

                return JsonResponse({
                    'status': 'success',
                    'message': 'Activate successfully!'
                }, status=status.HTTP_200_OK)
            else:
                return JsonResponse({
                    'status': 'fail',
                    'message': 'User has been already activated'
                }, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return JsonResponse({
                    'status': 'fail',
                    'message': 'Activation Expired'
                }, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return JsonResponse({
                    'status': 'fail',
                    'message': 'Invalid token'
                }, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                request,
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password']
            )

            if user:

                if not user.is_verified:
                    return JsonResponse({
                        'status': 'fail',
                        'message': 'Your account isn\'t verified'
                    }, status=status.HTTP_400_BAD_REQUEST)

                refresh = TokenObtainPairSerializer.get_token(user)
                data = {
                    'refresh_token': str(refresh),
                    'access_token': str(refresh.access_token)
                }

                return JsonResponse({
                    'status': 'success',
                    'message': 'Login successfully',
                    'data': data
                }, status=status.HTTP_200_OK)

            return JsonResponse({
                'status': 'fail',
                'message': 'Email or password is incorrect!'
            }, status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse({
            'status': 'error',
            'message': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class UserChangePasswordView(APIView):
    permission_classes = (IsAuthenticated, UserVerifyPermission)

    def post(self, request):
        serializer = UserChangePasswordSerializer(data=request.data)
        if serializer.is_valid():

            if request.user.check_password(serializer.validated_data['old_password']):
                request.user.set_password(serializer.validated_data['new_password'])
                request.user.save()

                return JsonResponse({
                    'status': 'success',
                    'message': 'Change password successfully!'
                }, status=status.HTTP_201_CREATED)

            else:
                return JsonResponse({
                    'status': 'fail',
                    'message': 'old password is not correct'
                }, status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse({
            'status': 'error',
            'message': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class UserResetPasswordView(APIView):

    def post(self, request):
        serializer = UserResetPasswordSerializer(data=request.data)
        if serializer.is_valid():


            user_email = User.objects.filter(email=serializer.validated_data['email'])

            if user_email:

                email = serializer.validated_data['email']
                totp = pyotp.TOTP(generate_key(email), interval=300)
                otp_code = totp.now()

                email_body = f"""
                    Hi {email},
                    This is the code for reseting your password.
                    This code is valid for 5 minutes.
                    The code: {otp_code}
                """

                data = {
                    'email_body': email_body, 
                    'to_email': email,
                    'email_subject': 'Reset your password'
                }

                EmailSending.send_email(data)

                return JsonResponse({
                    'status': 'success',
                    'message': 'The valid code has been sent your inbox'
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return JsonResponse({
                    'status': 'fail',
                    'message': 'This email does not belong to any accounts'
                }, status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse({
            'status': 'error',
            'message': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class UserResetConfirmPasswordView(APIView):

    def post(self, request):
        serializer = UserResetConfirmPasswordSerializer(data=request.data)
        if serializer.is_valid():

            # Check OTP code
            otp_code = serializer.validated_data['code']
            totp = pyotp.TOTP(generate_key(request.user.email), interval=300)

            if not totp.verify(otp_code):
                return JsonResponse({
                    'status': 'fail',
                    'message': 'Invalid code'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Reset user's password
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()

            return JsonResponse({
                'status': 'success',
                'message': 'Reset password successfully'
            }, status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse({
            'status': 'error',
            'message': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    permission_classes = (IsAuthenticated, UserVerifyPermission)

    def get(self, request):
        serializer = UserSerializer(request.user)
        return JsonResponse({
            'status': 'success',
            'message': 'Get detail of current user successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK, safe=False)

class UserDetailView(APIView):
    permission_classes = (IsAuthenticated, UserVerifyPermission)

    def get_object(self, pk):
        """
        Get a todo object by pk
        :param: pk -> int
        :return: todo.models.Todo
        """
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, user_id):
        user = self.get_object(user_id)
        serializer = UserSerializer(user)
        return JsonResponse({
            'status': 'success',
            'message': 'Get detail of a user successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

class UserListView(APIView):
    permission_classes = (IsAuthenticated, UserVerifyPermission)

    def get(self, request):
        users = User.objects.exclude(email = request.user.email)
        serializer = UserSerializer(users, many=True)
        return JsonResponse({
            'status': 'success',
            'message': 'Get all user successfully (exclude current user)',
            'data': serializer.data
        }, status=status.HTTP_200_OK)