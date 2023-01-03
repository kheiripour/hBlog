from django.contrib.sitemaps import Sitemap
from django.utils.timezone import now
from .models import Post


class BlogSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Post.objects.filter(status=True, pub_date__lte=now())

    def lastmod(self, obj):
        return obj.pub_date
