from django.core.management.base import BaseCommand
from faker import Faker
from random import choice
from os import listdir
from os.path import isfile, join

from core import settings
from accounts.models import Profile
from ...models import Post ,Category,Comment

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('number', type=int)

    def handle(self, *args, **options):

        number = options['number']
        fake = Faker()

        # posts = Post.objects.all()
        # images =[]
        # for p in posts:
        #     images.append(p.image)
        # print(images)

        media_path = join(settings.MEDIA_ROOT, "posts") 
        myfiles = [f for f in listdir(media_path) if isfile(join(media_path, f))]
        all_comments = 0

        for _ in range(number):
            post = Post.objects.create(
                title = fake.paragraph(nb_sentences=1),
                content = fake.paragraph(nb_sentences=15),
                snippet = fake.paragraph(nb_sentences=2),
                author = choice(Profile.objects.all()),
                status = True,
                image = join('posts',choice(myfiles))
                )
        
            cats = choice([1,2,3])
            for _ in range (cats):    
                post.category.add(choice((Category.objects.all())))
            
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
                    message = fake.paragraph(nb_sentences=choice(range(0,10))),
                    approved = True
                )
                all_comments += 1

        self.stdout.write(self.style.SUCCESS('Successfully added %i posts and %i comments :)' )%(number,all_comments))
                
            
            
         
