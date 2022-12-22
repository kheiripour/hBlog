from django.shortcuts import get_object_or_404
from django.views.generic import ListView,CreateView
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from datetime import datetime
from django.urls import reverse,reverse_lazy
from django.contrib import messages
from .models import Post,PostVersion,Comment,Category
from .forms import PostVersionForm
from accounts.models import Profile
class BlogList(ListView):
    template_name = "blog/blog-list.html"
    context_object_name = 'posts'
    model = Post
    paginate_by = 9
    extra_context = {}

    def get_queryset(self):
        posts = Post.objects.filter(status=True,pub_date__lte=datetime.now())

        if (p := self.kwargs.get('author_id')) is not None:
            posts = posts.filter(author__id=p)
 
        elif (p := self.kwargs.get('cat_id')) is not None:
            posts = posts.filter(active_version__category__id=p)

        elif (p := self.request.GET.get('search')) is not None:
            posts = posts.filter(active_version__content__contains=p)

        self.extra_context['count'] = len(posts)   
        for post in posts:
            post.title = post.active_version.title
            post.snippet = post.active_version.snippet
            post.category = post.active_version.category
            post.image = post.active_version.image
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
        post = get_object_or_404(Post,id=self.kwargs['pk'],status=True)
        context['title'] = post.active_version.title
        comments = Comment.objects.filter(post=post,approved=True)
        for comment in comments:
            if not comment.replied_to:
                comment.replies = comments.filter(replied_to=comment)
        post.title = post.active_version.title
        post.content = post.active_version.content
        post.snippet = post.active_version.snippet
        post.category = post.active_version.category
        post.image = post.active_version.image
        
        context['post'] = post
        context['comments'] = comments

        return context

    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post,id=self.kwargs['pk'])
        post.counted_view += 1
        post.save()
        return super().get(request, *args, **kwargs)
      
    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS,
                                 'Your Comment Submitted! Thank you')
        if self.request.user.is_authenticated:
            form.instance.commenter = self.request.user.profile
        else:
            form.instance.name = self.request.POST.get('name')


        form.instance.post = Post.objects.get(id=self.kwargs['pk'])

        if (rep:=(self.request.POST.get('replied_to_id'))):
            form.instance.replied_to = Comment.objects.get(id=rep)

        return super().form_valid(form)

class BlogAuthorList(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    permission_required = ('blog.add_postversion', 'blog.change_post', 'blog.add_post')
    template_name = "blog/blog-list.html"
    context_object_name = 'posts'
    model = Post
    paginate_by = 9
    extra_context = {'title':'MyPosts','resalt_title':'Your Posts'}

    def get_queryset(self):
        posts = Post.objects.filter(author=self.request.user.profile)

        self.extra_context['count'] = len(posts)   
        for post in posts:
            post.title = post.active_version.title
            post.snippet = post.active_version.snippet
            post.category = post.active_version.category
            post.image = post.active_version.image
            post.comments = Comment.objects.filter(post=post,approved=True).count()
            post.lastversion = PostVersion.objects.filter(post=post).order_by('-number').first()
            post.pend = True if post.active_version != post.lastversion else False    
            post.admin_checked = True if post.lastversion.admin_note else False
        return posts
        
class BlogAuthor(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    permission_required = ('blog.add_postversion', 'blog.change_post', 'blog.add_post')
    model = PostVersion
    template_name = "blog/blog-author.html"
    form_class = PostVersionForm
    success_url = reverse_lazy('blog:blog-myposts')

    def form_valid(self, form):
        post_version = form.save()

        if p:=self.kwargs.get('pk'):
            post = get_object_or_404(Post,id=p)
            pre_post_version = PostVersion.objects.filter(post=post).order_by('-number').first()
            post_version.number = pre_post_version.number + 1
            post_version.image = pre_post_version.image
            messages.add_message(self.request, messages.SUCCESS,
                                 'Your Change request sent successfully. Please wait for admin check, Thank You.')
        else:
            messages.add_message(self.request, messages.SUCCESS,
                                 'Your new post created successfully. Please wait for admin check, Thank You.')
            post = Post.objects.create(author = self.request.user.profile,active_version = post_version)   
            post_version.number = 1

        if img:=self.request.FILES.get('image'):
            post_version.image = img

        post_version.post = post

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if pk:=self.kwargs.get('pk'): 
            post = get_object_or_404(Post, id=pk, author=self.request.user.profile)
            post_version = PostVersion.objects.filter(post=post).order_by('-number').first()
            title = post_version.title
            snippet = post_version.snippet
            content = post_version.content
            category = post_version.category.all()
            author_note = post_version.author_note
            post.image = post_version.image
            form = PostVersionForm(
                {
                'title':title,
                'snippet':snippet,
                'content':content,
                'category':category,
                'author_note':author_note
                }
            )
            context['title'] = 'Edit Post V:%i-->V:%i'%(post_version.number,post_version.number + 1)
            context['form'] = form
            context['admin_note'] = post_version.admin_note
            context['post'] = post
            
        else:
            
            context['title'] = 'Create New Post'
        
        return context



