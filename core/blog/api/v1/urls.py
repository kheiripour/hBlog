from .views import *
from rest_framework.routers import DefaultRouter

app_name = "api-v1"

router = DefaultRouter()
router.register("blog",BlogModelViewSet , basename="blog")
router.register("author",AuthorModelViewSet , basename="author")

urlpatterns = router.urls
