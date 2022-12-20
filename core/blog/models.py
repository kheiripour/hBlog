from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save
from django.dispatch import receiver

from accounts.models import Profile
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class PostVersion(models.Model):
    post = models.ForeignKey('post',on_delete=models.CASCADE)
    number = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=255)
    content = models.TextField()
    snippet = models.TextField(default="Summary description for blogs page",max_length=150)
    category = models.ManyToManyField(Category,help_text="First will be main category")
    image = models.ImageField(upload_to='posts/',null=True,blank=True)

    author_note = models.TextField(blank=True)
    admin_note = models.TextField(blank=True)

    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.number) + "-" + self.title


class Post(models.Model):
    author = models.ForeignKey(Profile,on_delete=models.SET_NULL,null=True)
    counted_view = models.IntegerField(default=0)
    status = models.BooleanField(default=False) 

    pub_date = models.DateField(null=True, blank=True,auto_now_add=True)    
    
    active_version = models.ForeignKey(PostVersion,on_delete=models.SET_NULL,blank=True,null=True,related_name='+')

    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.id) + "-" + str(self.author)


    class   Meta:
        ordering = ['-created_date']



class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    commenter = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=20, blank=True)
    replied_to = models.ForeignKey("self", on_delete=models.SET_NULL,null=True,blank=True)
    message = models.TextField(blank=False)
    approved = models.BooleanField(default=False)

    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    

    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id) + "-" + str(self.commenter)

    class  Meta:
        ordering = ['-created_date']


@receiver(pre_save, sender=Comment)
def save_name(sender,instance,*args,**kwargs):
    if instance.commenter: instance.name = instance.commenter.__str__()