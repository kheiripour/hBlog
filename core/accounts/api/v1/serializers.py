from rest_framework import serializers
from django.contrib.auth.password_validation import (
    validate_password,
)
from django.core import exceptions
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    api_settings,
    update_last_login,
)
from ...models import User, Profile

class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializing  email and passwords and creating new user.
    """
    password1 = serializers.CharField(max_length=250, write_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "password1"]

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("password1"):
            raise serializers.ValidationError(
                {"detail": "password doesn't match"}
            )
        try:
            validate_password(attrs.get("password"))
        except exceptions.ValidationError as er:
            raise serializers.ValidationError({"password": er.messages})
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop("password1", None)
        return User.objects.create_user(**validated_data)

class ConfirmResendSerializer(serializers.Serializer):
    """
    Serializing  date for resending activation email.
    """
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        email = attrs.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"detail": "user does not exist"}
            )
        if user.is_verified:
            raise serializers.ValidationError(
                {"detail": "user is already verified"}
            )

        attrs["user"] = user
        return super().validate(attrs)

class ChangePasswordSerializer(serializers.Serializer):
    """
    Validate and serialize passwords for password change. 
    """
    oldpassword = serializers.CharField(required=True, max_length=250)
    newpassword1 = serializers.CharField(required=True, max_length=250)
    newpassword2 = serializers.CharField(required=True, max_length=250)

    def validate(self, attrs):
        if attrs.get("newpassword1") != attrs.get("newpassword2"):
            raise serializers.ValidationError(
                {"detail": "password doesnt match"}
            )
        try:
            validate_password(attrs.get("newpassword1"))
        except exceptions.ValidationError as er:
            raise serializers.ValidationError({"new password": er.messages})
        return super().validate(attrs)

class CustomAuthTokenSerializer(serializers.Serializer):
    """
    Validate and serialize email and password and then login.
    """
    email = serializers.EmailField(label=_("email"), write_only=True)
    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )
    token = serializers.CharField(label=_("Token"), read_only=True)

    def validate(self, attrs):
        username = attrs.get("email")
        password = attrs.get("password")
        if username and password:
            user = authenticate(
                request=self.context.get("request"),
                username=username,
                password=password,
            )
            if not user:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg, code="authorization")
            if not user.is_verified:
                raise serializers.ValidationError(
                    {"details": "user is not verified"}
                )
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code="authorization")
        attrs["user"] = user
        return attrs

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Generating jwt for auth and return it as string.
    """
    def validate(self, attrs):
        data = super().validate(attrs)
        if not self.user.is_verified:
            raise serializers.ValidationError(
                {"details": "user is not verified"}
            )
        refresh = self.get_token(self.user)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        data["email"] = str(self.user.email)
        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)
        return data

class PasswordResetSerializer(serializers.Serializer):
    """
    Validator of user existence to send reset password link
    """
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        email = attrs.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"detail": "user does not exist"}
            )
        attrs["user"] = user
        return super().validate(attrs)

class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Validating new passwords to reset password.
    """
    newpassword1 = serializers.CharField(required=True, max_length=250)
    newpassword2 = serializers.CharField(required=True, max_length=250)

    def validate(self, attrs):
        if attrs.get("newpassword1") != attrs.get("newpassword2"):
            raise serializers.ValidationError(
                {"detail": "password doesn't match"}
            )
        try:
            validate_password(attrs.get("newpassword1"))
        except exceptions.ValidationError as er:
            raise serializers.ValidationError({"new password": er.messages})
        return super().validate(attrs)

class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer of profile data for getting and updating. 
    It also provide absolute url of single profiles.
    """
    absolute_url = serializers.SerializerMethodField()
    class Meta:
        model = Profile
        fields = ['absolute_url','user','first_name','last_name','phone_number','address','image','about']
        read_only_fields = ['user']

    def get_absolute_url(self,obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.pk)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        request = self.context.get('request',None)
        if request.parser_context.get('kwargs').get('pk'):
            rep.pop('absolute_url', None)
        return rep