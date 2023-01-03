from django.template import Library
from datetime import datetime
from blog.models import Post, Category

register = Library()


@register.inclusion_tag("website/latest.html")
def main_latest(count):
    """
    Provide latest active published posts giving count argument and order by descending pub_date
    """
    posts = Post.objects.filter(status=True, pub_date__lte=datetime.now()).order_by(
        "-pub_date"
    )[:count]
    for post in posts:
        post.title = post.active_version.title
        post.snippet = post.active_version.snippet
        post.category = post.active_version.category
        post.image = post.active_version.image
    return {"posts": posts}


@register.inclusion_tag("website/categories.html")
def blog_categories():
    """
    Return categories count sorted by most counts.
    """
    posts = Post.objects.filter(status=True, pub_date__lte=datetime.now())
    categories = Category.objects.all()
    cat_dict = {}
    for cat in categories:
        count = posts.filter(active_version__category=cat).count()
        if count > 0:
            cat_dict[cat] = count
    cats = {
        k: v
        for k, v in sorted(cat_dict.items(), key=lambda item: item[1], reverse=True)
    }
    return {"cats": cats}
