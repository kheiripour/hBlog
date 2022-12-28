from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('profile',ProfileModelViewSet,basename='profile')

app_name = 'api-v1'

urlpatterns = [
    # registration:
    path(
        "registration/",
        RegistrationApiView.as_view(),
        name="registration",
    ),
    path(
        "confirm-activation/<str:token>",
        ConfirmActivation.as_view(),
        name="confirm-activation",
    ),
    path(
        "confirm-activation/resend/",
        ConfirmActivationResend.as_view(),
        name="confirm-activation-resend",
    ),
    # change password:
    path(
        "change-password/",
        ChangePasswordView.as_view(),
        name="change-password",
    ),
    # login token:
    path(
        "token/login/",
        CustomObtainAuthToken.as_view(),
        name="token-login",
    ),
    path(
        "token/logout/",
        CustomDiscardAuthToken.as_view(),
        name="token-logout",
    ),
    # login jwt
    path(
        "jwt/create/",
        CustomTokenObtainPairView.as_view(),
        name="jwt-create",
    ),
    path(
        "jwt/refresh/",
        TokenRefreshView.as_view(),
        name="jwt-refresh",
    ),
    path(
        "jwt/verify/",
        TokenVerifyView.as_view(),
        name="jwt-verify",
    ),
    # reset password:
    path(
        "reset_password/",
        ResetPasswordView.as_view(),
        name="reset-password",
    ),
    path(
        "reset_password_confirm/<str:token>",
        ResetPasswordConfirmView.as_view(),
        name="reset-password-confirm",
    ),
]

urlpatterns += router.urls