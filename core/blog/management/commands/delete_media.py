from django.core.management.base import BaseCommand
from faker import Faker
from random import choice
from os import listdir,remove
from os.path import isfile, join

from core import settings
from accounts.models import Profile
from ...models import Post,PostVersion ,Category,Comment

class Command(BaseCommand):


    def handle(self, *args, **options):


        media_path = join(settings.MEDIA_ROOT, "posts") 
        for f in listdir(media_path): 
            if isfile(join(media_path, f)):
                remove(join('/app/media/posts',f))
      
        # for f in myfiles:
        #     if f.isfile:
        #         remove(f)
            
            
         
