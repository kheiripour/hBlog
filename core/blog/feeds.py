from django.contrib.syndication.views import Feed
from .models import Post


class LatestEntriesFeed(Feed):
    title = "hblog newest Posts"
    link = "/sitenews/"
    description = "Be Update in coaching and positive energy subjects!"

    def items(self):
        return Post.objects.order_by("-pub_date")[:5]

    def item_title(self, item):
        return item.active_version.title

    def item_snippet(self, item):
        return item.active_version.snippet
