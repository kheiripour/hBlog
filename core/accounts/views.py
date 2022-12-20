from django.urls import reverse_lazy,reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView , UpdateView
from django.contrib.auth.views import (
    LoginView as BaseLoginView,)
from .forms import UserRegisterForm
from .models import Profile

class SignUpView(CreateView):
    template_name = "accounts/register.html"
    form_class = UserRegisterForm
    success_url = reverse_lazy("accounts:login")
    
class LoginView(BaseLoginView):
    template_name = "accounts/login.html"
    fields = ["email", "password"]
    
    def get_success_url(self):
        profile = Profile.objects.get(user=self.request.user)
        return "/" if profile.is_complete else reverse("accounts:profile")
     

class ProfileView(LoginRequiredMixin, UpdateView):
    template_name = "accounts/profile.html"
    model = Profile
    fields = ['first_name','last_name','about','address','phone_number','image']
    success_url = "/"

    def get_object(self):
        return get_object_or_404(Profile,user=self.request.user)

    def post(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=self.request.user)
        profile.is_complete = True
        profile.save()
        return super().post(request, *args, **kwargs)


      


    

