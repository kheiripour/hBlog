from django.shortcuts import get_object_or_404
from django.views.generic import ListView,CreateView
from datetime import date
from django.urls import reverse
from .models import Post,Comment,Category
from accounts.models import Profile
class BlogList(ListView):
    template_name = "blog/blog-list.html"
    context_object_name = 'posts'
    model = Post
    paginate_by = 9
    extra_context = {}

    def get_queryset(self):
        posts = Post.objects.filter(status=True,pub_date__lte=date.today())

        if (p := self.kwargs.get('author_id')) is not None:
            posts = posts.filter(author__id=p)
 
        elif (p := self.kwargs.get('cat_id')) is not None:
            posts = posts.filter(category__id=p)


        elif (p := self.request.GET.get('search')) is not None:
            posts = posts.filter(content__contains=p)

        self.extra_context['count'] = len(posts)   
        for post in posts:
            post.comments = Comment.objects.filter(post=post,approved=True).count()
        
        return posts
   
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Blogs"

        if (p := self.kwargs.get('author_id')) is not None:
            context['resalt_title'] = "Author"
            context['resalt_value'] = get_object_or_404(Profile,id=p)
        elif (p := self.kwargs.get('cat_id')) is not None:
            context['resalt_title'] = "Category"
            context['resalt_value'] = get_object_or_404(Category,id=p)
        elif (p := self.request.GET.get('search')) is not None:
            context['resalt_title'] = "Search"
            context['resalt_value'] = p
        
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

    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post,id=self.kwargs['pk'])
        post.counted_view += 1
        post.save()
        return super().get(request, *args, **kwargs)
      
    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.commenter = self.request.user.profile
        else:
            form.instance.name = self.request.POST.get('name')


        form.instance.post = Post.objects.get(id=self.kwargs['pk'])

        if (rep:=(self.request.POST.get('replied_to_id'))):
            form.instance.replied_to = Comment.objects.get(id=rep)

        return super().form_valid(form)
