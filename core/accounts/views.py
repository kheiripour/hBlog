from django.urls import reverse_lazy
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
    success_url = reverse_lazy("/")

class ProfileView(LoginRequiredMixin ,UpdateView,SuccessMessageMixin):
    template_name = "accounts/profile.html"
    model = Profile
    fields = ['first_name','last_name','about','address','phone_number']
    success_url = reverse_lazy("accounts:login")
    success_message = "Your profile updated successfully"

