from celery import shared_task
from django.utils.timezone import now, timedelta
from django.contrib.sites.models import Site
from mail_templated import EmailMessage
from website.utils import EmailThread
from website.models import Newsletter
from blog.models import Post


@shared_task
def send_new_posts():
    """
    This is task will send newsletter mail for subscribed users.
    It will run every night and contains news posts that had been published each day.
    """
    posts = Post.objects.filter(
        status=True,
        pub_date__date__lte=now(),
        pub_date__date__gte=now() - timedelta(days=1),
    )
    if posts:
        http = "http://"
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
        print(
            "Successfully %i posts emailed to %i users.... :)"
            % (len(posts), len(users))
        )
    else:
        print("There is no new posts to mail !")
