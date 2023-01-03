from rest_framework import viewsets, mixins, permissions, status
from rest_framework.response import Response
from django.utils.timezone import now 
from .serializer import ContactSerializer, NewsletterSerializer, SliderSerializer
from ...models import Slider


class ContactModelViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """
    Will create user's contact messages .
    """

    serializer_class = ContactSerializer
    permission_classes = [permissions.AllowAny]

    # If user is authenticated his profile data will use otherwise get name and email
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if request.user.is_authenticated:
            serializer.validated_data["sender"] = request.user.profile
            serializer.validated_data["name"] = request.user.profile.__str__()
            serializer.validated_data["email"] = request.user.email
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class NewsletterModelViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """
    Submit newsletter email form users.
    """

    serializer_class = NewsletterSerializer
    permission_classes = [permissions.AllowAny]


class SliderModelViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """
    Get list of active sliders posts with their summarized data.
    """

    serializer_class = SliderSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Slider.objects.filter(
        is_active=True, post__status=True, post__pub_date__lte=now()
    ).order_by("order")
