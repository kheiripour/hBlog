from django.db import models
from blog.models import Post
from accounts.models import Profile
from blog.models import Category
# Create your models here.

class Slider(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    snippet = models.TextField(max_length=200,blank=True,help_text="Leave it blank to use post snippet.")
    image = models.ImageField(upload_to='slider/',null=True,blank=True,help_text="Prefer 1300 x 500 size")
    order = models.PositiveBigIntegerField(blank=True,null=True)
    is_active = models.BooleanField(default=True)


class Contact(models.Model):
    sender = models.ForeignKey(Profile,on_delete=models.SET_NULL,null=True,blank=True,help_text="If this filed is empty, it means user were not authenticated.")
    name = models.CharField(max_length=255,blank=True)
    subject = models.CharField(max_length=255,default='')
    message = models.TextField()
    email = models.EmailField(blank=True)
    admin_note = models.TextField(blank=True,null=True)
    is_done = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    category = models.ManyToManyField(Category, blank=True)
    
    def __str__(self):
        return self.email

