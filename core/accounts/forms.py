from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions

User = get_user_model()

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    password1 = forms.CharField(max_length=100, label="Password", widget=forms.PasswordInput())
    password2 = forms.CharField(max_length=100, label="Confirm Password", widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ["email"]
class ForgetPasswordForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["email"]

    def is_valid(self):
        email = self.data.get("email")
        return User.objects.filter(email=email).exists()


class RestPasswordForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ["password1", "password2"]

    def is_valid(self):
        password1 = self.data.get("password1")
        password2 = self.data.get("password2")
        try:
            validate_password(password1)
        except exceptions.ValidationError as er:
            self.add_error(field=None, error=er.messages)
            return False
        if password1 != password2:
            self.add_error(field=None, error="Two passwords doesnt match")
            return False
        return True
