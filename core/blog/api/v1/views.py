from rest_framework import viewsets,mixins
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from datetime import datetime
from .permissions import IsAuthor
from .serializers import (CommentSerializer, BlogModelSerializer, PostVersionSerializer)
from .paginations import BlogPagination
from ...models import Post, PostVersion, Comment

class BlogModelViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A public viewset that gives all approved and published posts with card infos.
    Can be filtered by author, category and search request in content field.
    Commenting to post handled by an action. 
    """
    permission_classes = [AllowAny]
    queryset = Post.objects.filter(status=True, pub_date__lte=datetime.now())
    filter_backends = [DjangoFilterBackend,SearchFilter]
    filterset_fields = ['author','active_version__category']
    search_fields = ['active_version__content']
    pagination_class = BlogPagination

    # Overridden because of POST method of comment submit action. In comment case serializer must be CommentSerializer.
    def get_serializer_class(self):  
        if self.request.method == 'POST':  
            return CommentSerializer
        else:
            return BlogModelSerializer

    # Caching system to have better performance.60 secs for post list.
    @method_decorator(cache_page(60))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(detail=True, methods=['post'])
    def send_comment(self, request, pk=None):
        """
        This action handle comment like normal template base of app.
        If user authenticated the name and email will be his profile name and email.
        Otherwise name and email will be given by api request.
        """
        post = self.get_object()
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)

        if self.request.user.is_authenticated:
            commenter = self.request.user.profile 
            name = commenter
        else:
            commenter = None
            name = serializer.validated_data['name']
            if not name: return Response({'details':'name cant be empty.'},status=status.HTTP_400_BAD_REQUEST)
        replied_to = serializer.validated_data['replied_to']
        if replied_to and replied_to not in Comment.objects.filter(post=post):
            return Response({'details':'replied_to not valid, must be in post comments'},status=status.HTTP_400_BAD_REQUEST)

        Comment.objects.create(
            post=post,
            commenter=commenter,
            name=name,
            replied_to=replied_to,
            message=serializer.validated_data['message']
        )
        return Response({'details':'comment sent successfully.'},status=status.HTTP_201_CREATED)

class AuthorModelViewSet(viewsets.ReadOnlyModelViewSet,mixins.CreateModelMixin):
    """
    A restricted viewset for author users to view list of their posts, creating new posts and
    making change request for their existing posts. Change request handled by an action.
    It can be filtered like BlogModelViewSet.
    """
    permission_classes = [IsAuthor]
    serializer_class = BlogModelSerializer
    filter_backends = [DjangoFilterBackend,SearchFilter]
    filterset_fields = ['active_version__category']
    search_fields = ['active_version__content']
    pagination_class = BlogPagination

    # If user request a post editing api that isn't it's author will receive an 404 error.
    def get_queryset(self):
        return Post.objects.filter(author=self.request.user.profile)

    def get_serializer_class(self): 
        """
        If method is POST its a post version creation request so serializer should be PostVersionSerializer,
        otherwise its just getting list of posts so the serializer should be BlogModelSerializer.
        """ 
        if self.request.method == 'POST':  
            return PostVersionSerializer
        else:
            return BlogModelSerializer

    # In case of post creation firs a post create and then post version that will be the post active version.
    def create(self, request, *args, **kwargs):
        post = Post.objects.create(author=request.user.profile)
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['post'] = post
        serializer.validated_data['number'] =  1
        self.perform_create(serializer)
        post.active_version = PostVersion.objects.get(post=post)
        post.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
           
    @action(detail=True, methods=['get','post'])
    def change_request(self, request, pk=None):
        """
        This action support 2 methods. 'get' for getting all versions of a post and
        'post' method for creating change request. 
        """
        post = self.get_object()
        post_versions = PostVersion.objects.filter(post=post).order_by('-number')
        if request.method == 'GET':        
            return Response (PostVersionSerializer(post_versions,many=True,context={'request':request}).data,status=status.HTTP_200_OK)
        else:
            serializer = self.get_serializer_class()(data=request.data)
            serializer.is_valid(raise_exception=True)
            number = post_versions.first().number + 1
            post_version = PostVersion.objects.create(
                post=post,
                number=number,
                title=serializer.validated_data['title'],
                content=serializer.validated_data['content'],
                snippet=serializer.validated_data['snippet'],
                image=serializer.validated_data['image'],
                author_note=serializer.validated_data['author_note']    
            )
            for cat in serializer.validated_data['category']:
                post_version.category.add(cat)
            return Response ({'detail':'version request sent successfully'},status=status.HTTP_201_CREATED)