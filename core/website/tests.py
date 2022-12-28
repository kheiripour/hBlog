import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from accounts.models import User

@pytest.fixture
def fakeuser(): 
    user = User.objects.create_user(
    email="ad@ad.com",
    password="M@k123456")
    user.profile.is_author = True
    user.profile.save()
    return user

@pytest.fixture
def api_client():
    client = APIClient()
    return client
@pytest.mark.django_db
class TestAccountsApi:
    client = APIClient()

    # get slide in home page for all users
    def test_get_slides_200_status(self):
        url = reverse('website:api-v1:slider-list')
        response = self.client.get(url)
        assert response.status_code == 200

    # send contact message for anonymous user
    def test_post_contact_message_anonymous_201_status(self):
        url = reverse('website:api-v1:contact-list')
        data = {
            "name": "ahmad",
            "subject": "test",
            "message": "testing",
            "email": "test@test.com"
                }
        response = self.client.post(url,data)
        assert response.status_code == 201

      # send contact message for authenticated user
    def test_post_contact_message_authenticated_201_status(self,fakeuser):
        self.client.force_authenticate(user=fakeuser)
        url = reverse('website:api-v1:contact-list')
        data = {
            "subject": "test",
            "message": "testing",
                }
        response = self.client.post(url,data)
        assert response.status_code == 201

    # submit newsletter email
    def test_post_submit_newsletter_201_status(self):
        url = reverse('website:api-v1:newsletter-list')
        data = {
            "email": "test@test.com"
                }
        response = self.client.post(url,data)
        assert response.status_code == 201
  