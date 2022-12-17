from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView,CreateView
from .models import Post,Comment
from datetime import date
from django.urls import reverse
class BlogList(ListView):
    template_name = "blog/blog-list.html"
    context_object_name = 'posts'
    model = Post
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Blogs"
        posts = Post.objects.filter(status=True,pub_date__lte=date.today())
        for post in posts:
            post.comments = Comment.objects.filter(post=post,approved=True).count()
        context['posts'] = posts

        return context

class BlogDetail(CreateView):
    model = Comment
    fields = ['message']
    template_name = "blog/blog-single.html"

    def get_success_url(self):
        url = reverse('blog:blog-single',kwargs=self.kwargs)
        return url

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        post = get_object_or_404(Post,id=self.kwargs['pk'])
        context['title'] = post.title
        comments = Comment.objects.filter(post=post,approved=True)
        for comment in comments:
            if not comment.replied_to:
                comment.replies = comments.filter(replied_to=comment)
 
        context['post'] = post
        context['comments'] = comments

        return context

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.commenter = self.request.user.profile
        else:
            form.instance.name = self.request.POST.get('name')


        form.instance.post = Post.objects.get(id=self.kwargs['pk'])

        if (rep:=(self.request.POST.get('replied_to_id'))):
            form.instance.replied_to = Comment.objects.get(id=rep)

        return super().form_valid(form)
