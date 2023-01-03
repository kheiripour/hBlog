import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from accounts.models import User

@pytest.fixture
def fakeuser1(): 
    user = User.objects.create_user(
    email="ad@ad.com",
    password="M@k123456")
    user.profile.is_author = True
    user.profile.save()
    return user

@pytest.fixture
def fakeuser2(): 
    user = User.objects.create_user(
    email="mam@jad.com",
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

    # register new user
    def test_register_user_201_status(self):
        url = reverse('accounts:api-v1:registration')
        data = {
            "email": "aa@bb.com",
            "password": "Mk@123456",
            "password1": "Mk@123456",
            }
        response = self.client.post(url,data)
        assert response.status_code == 201
        
    #get profile from anonymous
    def test_anonymouse_get_profile_401_status(self,fakeuser1):
        profile = fakeuser1.profile
        url = reverse('accounts:api-v1:profile-detail',kwargs={'pk':profile.id})
        response = self.client.get(url)
        assert response.status_code == 401

    #get others profile
    def test_get_others_profile_404_status(self,fakeuser1,fakeuser2):
        profile = fakeuser1.profile
        self.client.force_authenticate(user=fakeuser2)
        url = reverse('accounts:api-v1:profile-detail',kwargs={'pk':profile.id})
        response = self.client.get(url)
        assert response.status_code == 404
    
       #get self profile
    def test_get_self_profile_200_status(self,fakeuser1):
        profile = fakeuser1.profile
        self.client.force_authenticate(user=fakeuser1)
        url = reverse('accounts:api-v1:profile-detail',kwargs={'pk':profile.id})
        response = self.client.get(url)
        assert response.status_code == 200

       #edit self profile
    def test_put_self_profile_200_status(self,fakeuser1):
        profile = fakeuser1.profile
        self.client.force_authenticate(user=fakeuser1)
        url = reverse('accounts:api-v1:profile-detail',kwargs={'pk':profile.id})
        data = {
            "user": profile.user,
            "first_name": "new name",
            "last_name": "nea last name",
            "phone_number": "+98912807"}
        response = self.client.put(url,data)
        assert response.status_code == 200