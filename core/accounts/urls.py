from django.urls import path, include
from django.urls import reverse_lazy
from .views import SignUpView, LoginView, ProfileView ,EmailSent,ConfirmActivation,ForgetPassword,ResetPassword
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

app_name = "accounts"

urlpatterns = [
    path("register/", SignUpView.as_view(), name="register"),
    path("activation-sent/", EmailSent.as_view(), name="email-sent"),
    path("activation-confirm/<str:token>", ConfirmActivation.as_view(), name="activation-confirm"),
    path("forget-password", ForgetPassword.as_view(), name="forget-password"),
    path("reset-password/<str:token>", ResetPassword.as_view(), name="reset-password"),
    path("login/", LoginView.as_view(), name="login"),
    path(
        "logout/",
        LogoutView.as_view(next_page=reverse_lazy("accounts:login")),
        name="logout",
    ),
    path("profile/", ProfileView.as_view(), name="profile"),

    path("api/v1/", include("accounts.api.v1.urls")),
    # path('', include('django.contrib.auth.urls')),
]
