from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.contrib.auth.views import (
    LoginView as BaseLoginView,
)
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from jwt import ExpiredSignatureError, InvalidSignatureError
from mail_templated import EmailMessage
from django.contrib import messages
from django.contrib.sites.models import Site
from core.settings import SECRET_KEY
from website.utils import EmailThread
from .forms import UserRegisterForm, ForgetPasswordForm, RestPasswordForm
from .models import Profile, User


def send_activation_code(request, user):
    """
    Send user activation code to user email, will reuse in some classes so written as public function.
    """
    refresh = RefreshToken.for_user(user)
    token = str(refresh.access_token)
    scheme = request.scheme
    host = Site.objects.get_current().domain
    email_obj = EmailMessage(
        "email/activation.html",
        {
            "token": token,
            "scheme": scheme,
            "host": host,
            "app_url": "/accounts/activation-confirm/",
        },
        "admin@admin.com",
        to=[user.email],
    )
    EmailThread(email_obj).start()


class SignUpView(CreateView):
    template_name = "accounts/register.html"
    form_class = UserRegisterForm
    success_url = reverse_lazy("accounts:email-sent")

    def form_valid(self, form):
        # When user registration form is valid, will try to send activation code to verify its real email.
        form.save()
        email = form.cleaned_data.get("email")
        user = User.objects.get(email=email)
        send_activation_code(self.request, user)
        self.request.session["email"] = email
        return super().form_valid(form)


class EmailSent(TemplateView):
    """
    This view is for confirming message shown to user that an email sent for it.
    """

    template_name = "accounts/email-sent.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["email"] = self.request.session.get("email")
        return context


class ConfirmActivation(TemplateView):
    """
    When user request activation by getting confirm url, this view validate its JWT and response to it.
    """

    template_name = "accounts/activation-confirm.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        token = kwargs.get("token")
        try:
            de_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user = get_object_or_404(User, id=de_token.get("user_id"))
            if user.is_verified:
                context["confirm_message"] = "User is already verified!"
            else:
                user.is_verified = True
                user.save()
                context["confirm_message"] = "User is verified successfully."
            context["status"] = True
        except ExpiredSignatureError:
            context["confirm_message"] = "Token is expired!"

        except InvalidSignatureError:
            context["confirm_message"] = "Token is invalid!"
        except Exception as e:
            context["confirm_message"] = str(e)
        return context

class LoginView(BaseLoginView):
    """
    If user is verified and credentials is true will login
    If its first time login will redirect to profile page.
    IF not verified, a new activation link will send.
    """

    template_name = "accounts/login.html"
    fields = ["email", "password", "remember"]

    def get_success_url(self):
        profile = Profile.objects.get(user=self.request.user)
        return "/" if profile.is_complete else reverse("accounts:profile")

    def form_valid(self, form):
        email = form.cleaned_data.get("username")
        remember = form.data.get("remember", False)
        user = User.objects.get(email=email)
        if user.is_verified:
            if not remember:
                self.request.session.set_expiry(0)
            return super().form_valid(form)
        else:
            send_activation_code(request=self.request, user=user)
            form.add_error(
                field=None,
                error="Your User is not verified, an activation link sent to your email.",
            )
            return self.form_invalid(form)

class ForgetPassword(FormView):
    """
    A form simply give user email to send reset password link,
    If user exist then a link sent, otherwise an error raise to user.
    """

    template_name = "accounts/forget_password.html"
    form_class = ForgetPasswordForm
    success_url = reverse_lazy("accounts:email-sent")

    def form_valid(self, form):
        user = User.objects.get(email=form.data.get("email"))
        refresh = RefreshToken.for_user(user)
        token = str(refresh.access_token)
        scheme = self.request.scheme
        host = Site.objects.get_current().domain
        email_obj = EmailMessage(
            "email/reset_password.html",
            {
                "token": token,
                "scheme": scheme,
                "host": host,
                "app_url": "/accounts/reset-password/",
            },
            "admin@admin.com",
            to=[user.email],
        )
        EmailThread(email_obj).start()
        self.request.session["email"] = user.email
        return super().form_valid(form)

    def form_invalid(self, form):
        form.add_error(field="email", error="This user not exist")
        return super().form_invalid(form)


class ResetPassword(FormView):
    """
    After getting resetpassword url user will come to this page to
    give new password. If two passwords validated successfully password will change.
    """

    template_name = "accounts/reset_password.html"
    form_class = RestPasswordForm
    success_url = reverse_lazy("accounts:login")

    def form_valid(self, form):
        token = self.kwargs.get("token")
        try:
            de_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=de_token.get("user_id"))
        except ExpiredSignatureError:
            form.add_error(
                field=None, error="Token is expired! Request new link and try again."
            )
            return super().form_invalid(form)
        except InvalidSignatureError:
            form.add_error(field=None, error="Token is invalid")
            return super().form_invalid(form)
        except Exception as e:
            form.add_error(field=None, error=str(e))
            return super().form_invalid(form)
        else:
            user.set_password(form.data.get("password1"))
            user.save()
            messages.add_message(
                self.request, messages.SUCCESS, "Password changed successfully!"
            )
            return super().form_valid(form)


class ProfileView(LoginRequiredMixin, UpdateView):
    """
    Retrieve and update profile using this page
    """

    template_name = "accounts/profile.html"
    model = Profile
    fields = ["first_name", "last_name", "about", "address", "phone_number", "image"]
    success_url = "/"

    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)

    def post(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=self.request.user)
        profile.is_complete = True
        profile.save()
        return super().post(request, *args, **kwargs)
