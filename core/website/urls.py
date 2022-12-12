from django.urls import path, include
from .views import IndexView


app_name = "website"

urlpatterns = [
    path("",IndexView.as_view(),name='index'),
    

    # path("api/v1/", include("blog.api.v1.urls")),
]
   
