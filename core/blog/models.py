from django.db import models
from django.urls import reverse
from django.db.models.signals import pre_save
from django.dispatch import receiver
from accounts.models import Profile


class Category(models.Model):
    """
    Reference model for categories that are many-to-many field for post versions.
    """

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class PostVersion(models.Model):
    """
    Many-to_one foreign key for post. It stores all version of each post.
    """

    post = models.ForeignKey("post", on_delete=models.CASCADE, blank=True, null=True)
    number = models.PositiveSmallIntegerField(blank=True, null=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    snippet = models.TextField(
        default="Summary description for blogs page", max_length=150
    )
    category = models.ManyToManyField(Category, help_text="First will be main category")
    image = models.ImageField(upload_to="posts/", null=True, blank=True)

    author_note = models.TextField(blank=True)
    admin_note = models.TextField(blank=True)

    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.number) + "-" + self.title


class Post(models.Model):
    """
    Main model for posts that parents post versions.
    """

    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    counted_view = models.IntegerField(default=0, blank=True, null=True)
    status = models.BooleanField(default=False, blank=True)
    pub_date = models.DateTimeField(null=True, blank=True)
    active_version = models.ForeignKey(
        PostVersion, on_delete=models.SET_NULL, blank=True, null=True, related_name="+"
    )

    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id) + "-" + str(self.author)

    def get_absolute_url(self):
        return reverse("blog:blog-single", kwargs={"pk": self.id})

    class Meta:
        ordering = ["-pub_date"]


class Comment(models.Model):
    """
    Many-to-one to post model. contains all comments.
    """

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    commenter = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, null=True, blank=True
    )
    name = models.CharField(max_length=20, blank=True)
    replied_to = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True
    )
    message = models.TextField(blank=False)
    approved = models.BooleanField(default=False)

    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id) + "-" + str(self.commenter) + "-" + str(self.post.id)

    class Meta:
        ordering = ["-created_date"]


@receiver(pre_save, sender=Comment)
def save_name(sender, instance, *args, **kwargs):
    """
    This signal will write commenter's name from his profile if authenticated.
    """
    if instance.commenter:
        instance.name = instance.commenter.__str__()
