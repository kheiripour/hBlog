from django.urls import path, include
from django.urls import reverse_lazy
from .views import SignUpView, LoginView, ProfileView 
from django.contrib.auth.views import LogoutView

app_name = "accounts"

urlpatterns = [
    path("register/", SignUpView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path(
        "logout/",
        LogoutView.as_view(next_page=reverse_lazy("accounts:profile")),
        name="logout",
    ),
    path("profile/", ProfileView.as_view(), name="profile"),

    path("api/v1/", include("accounts.api.v1.urls")),
    # path('', include('django.contrib.auth.urls')),
]
