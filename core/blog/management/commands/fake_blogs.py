from django.core.management.base import BaseCommand
from faker import Faker
from random import choice
from os import listdir
from os.path import isfile, join

from core import settings
from accounts.models import Profile
from ...models import Post,PostVersion ,Category,Comment

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('number', type=int)

    def handle(self, *args, **options):

        number = options['number']
        fake = Faker()

        media_path = join(settings.MEDIA_ROOT, "posts") 
        myfiles = [f for f in listdir(media_path) if isfile(join(media_path, f))]
        all_comments = 0

        for _ in range(number):
            content_paras = choice(range(2,7))
            content = ""
            for _ in range(content_paras):
                content = content + "<p>" + fake.paragraph(nb_sentences=choice(range(10,20))) + "</p>"

            post = Post.objects.create(
            
                author = choice(Profile.objects.all()),
                status = True,
              
                )
            post_version = PostVersion.objects.create(
                post = post,
                number = 1,

                title = fake.paragraph(nb_sentences=1),
                content = content,
                snippet = fake.paragraph(nb_sentences=2),
                image = join('posts',choice(myfiles))
            )


            cats = choice([1,2,3])
            for _ in range (cats):    
                post_version.category.add(choice((Category.objects.all())))

            post.active_version = post_version
            post.save()
            
            comments = choice(range(0,10))
            for _ in range(comments):
                replied_to = None
                is_reply = choice([True,False])
                parent_comments = Comment.objects.filter(post=post,replied_to=None)
                if is_reply and parent_comments: 
                    replied_to = choice(parent_comments)
                Comment.objects.create(
                    post = post,
                    commenter = choice(Profile.objects.all()),
                    replied_to = replied_to,
                    message = fake.paragraph(nb_sentences=choice(range(1,10))),
                    approved = True
                )
                all_comments += 1

        self.stdout.write(self.style.SUCCESS('Successfully added %i posts and %i comments :)' )%(number,all_comments))
                
            
            
         
