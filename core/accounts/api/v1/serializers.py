from ...models import User, Profile
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.exceptions import ValidationError as PasswordValidationError
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'confirm_password')

    def validate(self, attrs):
        email = attrs.get('email', '')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': 'Email already exists'})

        password = attrs.get('password', '')
        confirm_password = attrs.get('confirm_password', '')
        try:
            validate_password(password, confirm_password)
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({'password': e.messages})
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop('confirm_password', None)
        return User.objects.create_user(**validated_data)


class CustomAuthTokenSerializer(serializers.Serializer):

    email = serializers.CharField(
        label=_("Email"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        username = attrs.get('email')
        password = attrs.get('password')

        if username is None or password is None:
            raise serializers.ValidationError(
                _('Must include "email" and "password".')
            )
        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
            if not user.is_verified:
                raise serializers.ValidationError({'is_verified': 'user is not verified'})

        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        if not self.user.is_verified:
            raise serializers.ValidationError({'is_verified': 'user is not verified'})
        data['user_id'] = self.user.id
        data['email'] = self.user.email
        return data


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(style={'input_type': 'password'}, write_only=True, required=True)
    new_password = serializers.CharField(style={'input_type': 'password'}, write_only=True, required=True)
    new_password1 = serializers.CharField(style={'input_type': 'password'}, write_only=True, required=True)

    def validate(self, attrs):
        user = self.context['request'].user

        old_password = attrs.get('old_password')
        new_password = attrs.get('new_password')
        new_password1 = attrs.get('new_password1')

        # Check old password
        if not user.check_password(old_password):
            raise serializers.ValidationError({'old_password': _('Wrong password.')})

        # Check if new passwords match
        if new_password != new_password1:
            raise serializers.ValidationError({'new_password': _('New passwords do not match.')})

        # Validate new password
        try:
            validate_password(new_password)
        except PasswordValidationError as e:
            raise serializers.ValidationError({'new_password': list(e.messages)})

        return super().validate(attrs)


class ProfileSerializer(serializers.ModelSerializer):
    email= serializers.CharField(source='user.email', read_only=True)
    class Meta:
        model = Profile
        fields = ('id', 'first_name', 'last_name', 'email', 'description', 'image')


class ResendActivationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, attrs):
        """Validate that the email is associated with a registered user."""

        email = attrs.get("email")
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"detail": "user does not exist"})
        if user_obj.is_verified:
            raise serializers.ValidationError(
                {"detail": "user is already activated and verified"}
            )
        attrs["user"] = user_obj
        return super().validate(attrs)
