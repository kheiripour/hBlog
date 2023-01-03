from django.core.management.base import BaseCommand
from datetime import date
from django.contrib.sites.models import Site
from mail_templated import EmailMessage
from blog.models import Post
from ...utils import EmailThread 
from ...models import Newsletter

class Command(BaseCommand):
    """
    Manually can run this command to email newsletter.
    """
    def handle(self, *args, **options):
        posts = Post.objects.filter(status=True,pub_date__date=date.today())
        if posts:
            http = 'http://'
            domain = Site.objects.get_current().domain
            users = list(Newsletter.objects.all())
            for post in posts:
                post.full_url = http + domain + post.get_absolute_url()
                post.title = post.active_version.title
            email_obj = EmailMessage(
            "email/newsletter.html",
            {
                "posts": posts,
            },
            "admin@admin.com",
            to=users,
            )
            EmailThread(email_obj).start()
            
            self.stdout.write(self.style.SUCCESS('Successfully %i posts emailed to %i users.... :)'%(len(posts),len(users)) ))
        else:
            self.stdout.write(self.style.ERROR('There is no new posts to mail!' ))       