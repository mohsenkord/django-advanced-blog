import threading
import jwt

from django.conf import settings
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView


from .serializers import (
    UserRegistrationSerializer, CustomAuthTokenSerializer, CustomTokenObtainPairSerializer,
    ChangePasswordSerializer,ProfileSerializer, ResendActivationSerializer,
)
from django.contrib.auth import get_user_model
from ...models import Profile
from mail_templated import EmailMessage
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import gettext as _
User = get_user_model()


class BaseActivationAPIView:
    """Base class to handle activation email sending."""

    def send_activation_email(self, user):
        token = self.get_tokens_for_user(user)
        email_obj = EmailMessage(
            'email/activation_email.tpl',
            {'token': token, 'confirmation_link': f'http://127.0.0.1:8000/accounts/api/v1/activation/confirm/{token}'},
            'admin@admin.com',
            to=[user.email]
        )
        email_thread = threading.Thread(target=self.send_email, args=(email_obj,))
        email_thread.start()

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class RegisterAPIView(generics.GenericAPIView, BaseActivationAPIView):
    """View for registering new user"""
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = {
            "user": {
                'email': user.email,
            },
            "message": _("User successfully registered. Please check your email to confirm your registration."),
        }
        self.send_activation_email(user)
        return Response(data, status=status.HTTP_201_CREATED)


class CustomAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


class CustomDestroyAuthToken(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class ChangePasswordView(generics.GenericAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileAPIView(generics.RetrieveUpdateAPIView):
    """View for getting profile"""
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    queryset = Profile.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj


def send_email(message):
    message.send()


class SendEmailView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        email_obj = EmailMessage('email/hello.tpl', {'user': 'mohsen'}, 'admin@admin.com',
                               to=['mohsen@gmail.com'])
        email_thread = threading.Thread(target=send_email, args=(email_obj,))
        email_thread.start()
        return Response({"message": "Email sent successfully"}, status=status.HTTP_200_OK)


class ActivationAPIView(APIView):

    def get(self, request, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({"message": "User activated successfully"}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({"message": "Activation Expired"}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({"message": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


class ResendActivationAPIView(generics.GenericAPIView, BaseActivationAPIView):
    serializer_class = ResendActivationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = get_object_or_404(User, email=serializer.validated_data['email'])

        if not user.is_verified:
            self.send_activation_email(user)
            return Response({"message": "Activation link sent successfully"}, status=status.HTTP_200_OK)

        return Response({"message": "User already activated"}, status=status.HTTP_400_BAD_REQUEST)