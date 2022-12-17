from django.db import models
from blog.models import Post
# Create your models here.

class Slider(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    snippet = models.TextField(default="Summary description for blogs page",max_length=200,blank=True,help_text="Leave it blank to use post snippet.")
    image = models.ImageField(upload_to='slider/',null=True,blank=True,help_text="Prefer 1300 x 500 size")
    is_active = models.BooleanField(default=True)
