from .views import (ContactModelViewSet, NewsletterModelViewSet, SliderModelViewSet )
from rest_framework.routers import DefaultRouter

app_name = 'api-v1'

router = DefaultRouter()
router.register('contact',ContactModelViewSet,basename='contact')
router.register('newsletter', NewsletterModelViewSet,basename='newsletter')
router.register('slider', SliderModelViewSet,basename='slider')

urlpatterns = router.urls