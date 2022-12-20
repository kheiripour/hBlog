from django.template import Library
from blog.models import Post,Category

register = Library()

@register.inclusion_tag('website/latest.html')
def main_latest(count):
    posts=Post.objects.filter(status=True)[:count]
    for post in posts:
        post.title = post.active_version.title
        post.snippet = post.active_version.snippet
        post.category = post.active_version.category
        post.image = post.active_version.image
    return {'posts':posts}


@register.inclusion_tag('website/categories.html')
def blog_categories():
    posts = Post.objects.filter(status=True)
    categories = Category.objects.all()
    cat_dict ={}
    for cat in categories:
        count = posts.filter(active_version__category=cat).count()
        if count>0: cat_dict[cat]=count
    cats={k: v for k, v in sorted(cat_dict.items(), key=lambda item: item[1],reverse=True)}
    return {'cats':cats}