from django.template import Library
from blog.models import Post,Category

register = Library()

@register.inclusion_tag('website/latest.html')
def main_latest(count):
    posts=Post.objects.filter(status=True)[:count]
    return {'posts':posts}


@register.inclusion_tag('website/categories.html')
def blog_categories():
    posts = Post.objects.filter(status=True)
    categories = Category.objects.all()
    cat_dict ={}
    for cat in categories:
        count = posts.filter(category=cat).count()
        if count>0: cat_dict[cat]=count
    cats={k: v for k, v in sorted(cat_dict.items(), key=lambda item: item[1],reverse=True)}
    return {'cats':cats}