from rest_framework.routers import DefaultRouter
from .views import BlogModelViewSet, AuthorModelViewSet

app_name = "api-v1"

router = DefaultRouter()
router.register("blog", BlogModelViewSet, basename="blog")
router.register("author", AuthorModelViewSet, basename="author")

urlpatterns = router.urls
