import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.templatetags.static import static
from django.utils.timezone import now ,timedelta
from django.utils.timezone import timedelta,now
from accounts.models import User
from .models import Post, PostVersion, Category, Comment


@pytest.fixture
def fakeuser1():
    user = User.objects.create_user(email="ad@ad.com", password="M@k123456")
    user.profile.is_author = True
    user.profile.save()
    return user


@pytest.fixture
def fakeuser2():
    user = User.objects.create_user(email="mam@jad.com", password="M@k123456")
    user.profile.is_author = True
    user.profile.save()
    return user


@pytest.fixture
def fakecats():
    cat1 = Category.objects.create(name="cat1")
    cat2 = Category.objects.create(name="cat2")
    return (cat1, cat2)


@pytest.fixture
def fakepost(fakeuser1, fakecats):
    user = fakeuser1
    cats = fakecats
    post = Post.objects.create(
        author=user.profile,
        status=True,
        pub_date=now()-timedelta(days=1)
    )
    post_version = PostVersion.objects.create(
        post=post,
        number=1,
        title="test title",
        content="test content",
        snippet="test snippet",
        image=static("default-post.jpg"),
    )
    post_version.category.add(cats[0])
    post_version.category.add(cats[1])
    post.active_version = post_version
    post.save()
    return post


@pytest.fixture
def fakecomment(fakeuser1, fakepost):
    comment = Comment.objects.create(
        post=fakepost, commenter=fakeuser1.profile, name="", message="nice post"
    )
    return comment


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.mark.django_db
class TestBlogApi:
    # get list of posts:
    def test_get_all_post_response_200_status(self, api_client):
        url = reverse("blog:api-v1:blog-list")
        response = api_client.get(url)
        assert response.status_code == 200

    # get a post detail
    def test_get_post_detail_status_200(self, api_client, fakepost):
        post = fakepost
        url = reverse("blog:api-v1:blog-detail", kwargs={"pk": post.id})
        response = api_client.get(url)
        assert response.status_code == 200

    # sending an anonymous comment
    def test_send_anonymous_comment_201_status(self, api_client, fakepost, fakecomment):
        post = fakepost
        url = reverse("blog:api-v1:blog-send-comment", kwargs={"pk": post.id})
        data = {
            "name": "ahmad",
            "message": "thats great post",
            "replied_to": fakecomment.id,
        }
        response = api_client.post(url, data)
        assert response.status_code == 201

    # sending an authenticated comment
    def test_send_authenticated_comment_201_status(
        self, api_client, fakepost, fakeuser1
    ):
        post = fakepost
        api_client.force_authenticate(user=fakeuser1)
        url = reverse("blog:api-v1:blog-send-comment", kwargs={"pk": post.id})
        data = {"name": "", "message": "thats great post", "replied_to": ""}
        response = api_client.post(url, data)
        assert response.status_code == 201

    # get list of my posts:
    def test_get_my_posts_response_200_status(self, api_client, fakeuser1):
        api_client.force_authenticate(user=fakeuser1)
        url = reverse("blog:api-v1:author-list")
        response = api_client.get(url)
        assert response.status_code == 200

    # get one of my post
    def test_get_mypost_detail__status_200(self, api_client, fakepost, fakeuser1):
        api_client.force_authenticate(user=fakeuser1)
        post = fakepost
        url = reverse("blog:api-v1:author-detail", kwargs={"pk": post.id})
        response = api_client.get(url)
        assert response.status_code == 200

    # change request send (creating new post_version)
    def test_change_request_send_201_status(self, api_client, fakepost, fakeuser1):
        post = fakepost
        api_client.force_authenticate(user=fakeuser1)
        url = reverse("blog:api-v1:author-change-request", kwargs={"pk": post.id})

        data = {
            "title": "new title",
            "content": "<p>new content </p> ",
            "snippet": "new snippet",
            "category": [1, 2],
            "image": "",
            "author_note": "test note",
        }
        response = api_client.post(url, data)
        assert response.status_code == 201

    # get all versions of a post by it's author
    def test_change_request_get_allversions_200_status(
        self, api_client, fakepost, fakeuser1
    ):
        post = fakepost
        api_client.force_authenticate(user=fakeuser1)
        url = reverse("blog:api-v1:author-change-request", kwargs={"pk": post.id})
        response = api_client.get(url)
        assert response.status_code == 200

    # prevent non-author user to send change request of a post
    def test_non_author_change_request_send_404_status(
        self, api_client, fakepost, fakeuser2
    ):
        post = fakepost
        api_client.force_authenticate(user=fakeuser2)
        url = reverse("blog:api-v1:author-change-request", kwargs={"pk": post.id})

        data = {
            "title": "new title",
            "content": "<p>new content </p> ",
            "snippet": "new snippet",
            "category": [1, 2],
            "image": "",
            "author_note": "test note",
        }
        response = api_client.post(url, data)
        assert response.status_code == 404
