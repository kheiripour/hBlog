from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('contact',ContactModelViewSet,basename='contact')
router.register('newsletter', NewsletterModelViewSet,basename='newsletter')

app_name = 'api-v1'

urlpatterns = router.urls