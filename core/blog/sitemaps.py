from django.contrib.sitemaps import Sitemap
from datetime import datetime
from .models import Post

class BlogSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Post.objects.filter(status=True, pub_date__lte=datetime.now())

    def lastmod(self, obj):
        return obj.pub_date