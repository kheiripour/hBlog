from django.db import models
from accounts.models import Profile

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(Profile,on_delete=models.SET_NULL,null=True)
    counted_view = models.IntegerField(default=0)
    status = models.BooleanField(default=False) 
    category = models.ManyToManyField(Category)
    image = models.ImageField(upload_to='lessons/',null=True,blank=True)     
    
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.id) + "-" + self.title

    class   Meta:
        ordering = ['-created_date','title']


class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    commenter = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    replied_to = models.ForeignKey("self", on_delete=models.SET_NULL,null=True,blank=True)
    message = models.TextField()
    approved = models.BooleanField(default=False)

    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id) + "-" + str(self.commenter)

    class   Meta:
        ordering = ['-created_date']