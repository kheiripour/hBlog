from django.urls import path, include
from .views import BlogList,BlogDetail


app_name = "blog"

urlpatterns = [
    path('',BlogList.as_view(),name='blog-list'),
    path('category/<int:cat_id>', BlogList.as_view(),name='blog-category'),
    path('author/<int:author_id>', BlogList.as_view(),name='blog-author'),
    path('<int:pk>/',BlogDetail.as_view(),name='blog-single'),    
    # path("api/v1/", include("blog.api.v1.urls")),
]
   
