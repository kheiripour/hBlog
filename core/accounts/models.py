from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class UserManager(BaseUserManager):
    """
    custom user model manager where email is the unique identifier
    """

    def create_user(self, email, password, **extra_fields):
        """
        create and save a user with the given email and password and extra fields
        """
        if not email:
            raise ValueError(_("the Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        create and save a SuperUser with given email and password
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_verified", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("super user must be staff"))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("super user must be superuser = true"))

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_author = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255,null=True)
    address = models.TextField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True)
    about = models.TextField(blank=True, null=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        if (name := str(self.first_name) + " " + str(self.last_name)) != " ":
            return name
        else:
            return self.user.email


@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
