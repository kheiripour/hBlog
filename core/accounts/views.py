from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import (
    SuccessMessageMixin,)
from django.views.generic.edit import CreateView , UpdateView
from django.contrib.auth.views import (
    LoginView as BaseLoginView,)
from .forms import UserRegisterForm
from .models import Profile


class SignUpView(CreateView):
    template_name = "accounts/register.html"
    form_class = UserRegisterForm

    def get_success_url(self):
        profile = Profile.objects.get(user=self.object)
        success_url = reverse_lazy("accounts:profile", kwargs={'pk':profile.id})
        return success_url 


class LoginView(BaseLoginView):
    template_name = "accounts/login.html"
    fields = ["email", "password"]
    # success_url = reverse_lazy("/")

class ProfileView(LoginRequiredMixin, UpdateView):
    template_name = "accounts/profile.html"
    model = Profile
    fields = ['first_name','last_name','about','address','phone_number','image']
    success_url = reverse_lazy("accounts:login") # will changed after blog implemented

    def get_object(self):
        return get_object_or_404(Profile.objects.all(),user=self.request.user)


      


    

