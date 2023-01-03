from django.urls import path, include
from .views import IndexView, ContactView


app_name = "website"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("contact/", ContactView.as_view(), name="contact"),
    path("api/v1/", include("website.api.v1.urls")),
]
