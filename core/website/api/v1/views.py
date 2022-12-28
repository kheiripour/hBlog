from rest_framework import viewsets, mixins, permissions, status
from rest_framework.response import Response
from .serializer import ContactSerializer, NewsletterSerializer


class ContactModelViewSet(viewsets.GenericViewSet,mixins.CreateModelMixin):
    serializer_class = ContactSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if request.user.is_authenticated:
            serializer.validated_data['sender'] = request.user.profile
            serializer.validated_data['name'] = request.user.profile.__str__()
            serializer.validated_data['email'] = request.user.email
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class NewsletterModelViewSet(viewsets.GenericViewSet,mixins.CreateModelMixin):
    serializer_class = NewsletterSerializer
    permission_classes = [permissions.AllowAny]
