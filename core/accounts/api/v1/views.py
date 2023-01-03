from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets, mixins
import jwt
from django.core.exceptions import ObjectDoesNotExist
from jwt import ExpiredSignatureError, InvalidSignatureError
from django.shortcuts import get_object_or_404
from mail_templated import EmailMessage
from django.contrib.sites.models import Site
from core.settings import SECRET_KEY
from website.utils import EmailThread
from .serializers import (RegistrationSerializer, ConfirmResendSerializer, ChangePasswordSerializer, CustomAuthTokenSerializer, CustomTokenObtainPairSerializer, PasswordResetSerializer, PasswordResetConfirmSerializer, ProfileSerializer)
from ...models import User, Profile

class RegistrationApiView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer
    """
    To get email and passwords and make new user if valid.
    If user created, activation code will send and profile will create.
    """
    def post(self, request, *arg, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        serializer.save()
        user_obj = get_object_or_404(User, email=email)
        token = self.get_tokens_for_user(user_obj) 
        scheme = request.scheme
        host = Site.objects.get_current().domain
        email_obj = EmailMessage(
            "email/activation.html",
            {
                "token": token,
                "scheme": scheme,
                "host": host,
                "app_url": '/accounts/api/v1/confirm-activation/',
            },
            "admin@admin.com",
            to=[email],
        )
        EmailThread(email_obj).start()
        return Response({"email": email}, status=status.HTTP_201_CREATED)

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

class ConfirmActivation(APIView):
    """
    Validating jwt given by activation link and verify user.
    """    
    def get(self, request, token):
        try:
            token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user = get_object_or_404(User, id=token.get("user_id"))
        except ExpiredSignatureError:
            return Response(
                {"details": "token is expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except InvalidSignatureError:
            return Response(
                {"details": "token is invalid"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user.is_verified:
            return Response({"details": "user is already verified"})
        user.is_verified = True
        user.save()
        return Response({"details": "user is verified successfully"})


class ConfirmActivationResend(generics.GenericAPIView):
    """
    In case of new activation link need for user. we will send it again using this view.
    """
    serializer_class = ConfirmResendSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token = self.get_tokens_for_user(user)
        scheme = request.scheme
        host = Site.objects.get_current().domain
        email_obj = EmailMessage(
            "email/activation.html",
            {
                "token": token,
                "scheme": scheme,
                "host": host,
                "app_url": '/accounts/api/v1/confirm-activation/',
            },
            "admin@admin.com",
            to=[user.email],
        )
        EmailThread(email_obj).start()
        return Response(
            {"details": "User activation resent successfully"},
            status=status.HTTP_200_OK,
        )

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

class ChangePasswordView(generics.GenericAPIView):
    """
    This view is for when a user is authenticated and want to change password. 
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def put(self, request, *args, **kwargs):
        self.object = self.request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not self.object.check_password(serializer.data.get("oldpassword")):
            return Response(
                {"old_password": "Wrong current password."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        self.object.set_password(serializer.data.get("newpassword1"))
        self.object.save()
        return Response(
            {"detail": "Password changed successfully"},
            status=status.HTTP_200_OK,
        )

class CustomObtainAuthToken(ObtainAuthToken):
    """
    Create auth token to login by token instead of basic authentication.
    """
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token = Token.objects.get_or_create(user=user)[0]
        return Response(
            {
                "token": token.key,
                "user_id": user.id,
                "email": user.email,
            }
        )
class CustomDiscardAuthToken(APIView):
    """
    Delete user auth token stored in token table.
    It also can be assumed as token logout.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()
        except ObjectDoesNotExist:
            return Response(
                {"details": "user does not have token"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(status=status.HTTP_204_NO_CONTENT)

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    jwt generator. it will return access, refresh and user email.
    """
    serializer_class = CustomTokenObtainPairSerializer
class ResetPasswordView(generics.GenericAPIView):
    """
    Send reset password email by jwt token.
    """
    serializer_class = PasswordResetSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)
        token = refresh.access_token
        scheme = request.scheme
        host = Site.objects.get_current().domain
        email_obj = EmailMessage(
            "email/reset_password.html",
            {
                "token": token,
                "scheme": scheme,
                "host": host,
                "app_url": '/accounts/api/v1/reset_password_confirm/',
            },
            "admin@admin.com",
            to=[user.email],
        )
        EmailThread(email_obj).start()
        return Response(
            {"details": "Reset password link resent successfully"},
            status=status.HTTP_200_OK,
        )

class ResetPasswordConfirmView(generics.GenericAPIView):
    """
    Receiving reset password url, validate jwt, check new passwords and finally change password.
    """
    serializer_class = PasswordResetConfirmSerializer

    def put(self, request, token):
        try:
            de_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user = get_object_or_404(User, id=de_token.get("user_id"))
        except ExpiredSignatureError:
            return Response(
                {"details": "token is expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except InvalidSignatureError:
            return Response(
                {"details": "token is invalid"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.data.get("newpassword1"))
        user.save()
        return Response(
            {"detail": "Password has been reset successfully"},
            status=status.HTTP_200_OK,
        )

class ProfileModelViewSet(viewsets.GenericViewSet,mixins.UpdateModelMixin,mixins.ListModelMixin,mixins.RetrieveModelMixin):
    """
    Get and update user profile data.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer
    
    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)