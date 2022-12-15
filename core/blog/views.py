from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView,DetailView
from .models import Post,Comment
from datetime import date
class BlogList(ListView):
    template_name = "blog/blog-list.html"
    context_object_name = 'posts'
    model = Post
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Blogs"
        posts = Post.objects.filter(status=True,pub_date__lte=date.today())
        for post in posts:
            post.comments = Comment.objects.filter(post=post,approved=True).count()
        context['posts'] = posts

        return context

class BlogDetail(DetailView):
    context_object_name = 'post'
    model = Post
    template_name = "blog/blog-single.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = get_object_or_404(Post,id=self.kwargs['pk'])
        context['title'] = post.title
        comments = Comment.objects.filter(post=post,approved=True)
        context['comments_counts'] = comments.count()
        for comment in comments:
            if not comment.replied_to:
                comment.replies = comments.filter(replied_to=comment)
 
        context['post'] = post
        context['comments'] = comments

        return context

