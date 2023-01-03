from django.shortcuts import get_object_or_404
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.utils.timezone import now 
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from .models import Post, PostVersion, Comment, Category
from .forms import PostVersionForm
from accounts.models import Profile


class BlogList(ListView):
    """
    Will use for all users to see all posts that published. Search results and filtration
    will be shown here.
    """

    template_name = "blog/blog-list.html"
    context_object_name = "posts"
    model = Post
    paginate_by = 9
    extra_context = {}

    def get_queryset(self):
        posts = Post.objects.filter(status=True, pub_date__lte=now())

        # Author filtration
        if (key := self.kwargs.get("author_id")) is not None:
            posts = posts.filter(author__id=key)

        # Category filtration
        elif (key := self.kwargs.get("cat_id")) is not None:
            posts = posts.filter(active_version__category__id=key)

        # Search result
        elif (key := self.request.GET.get("search")) is not None:
            posts = posts.filter(active_version__content__contains=key)

        self.extra_context["count"] = len(posts)

        # Adding post attributes from it's active version for post cards in blog list.
        for post in posts:
            post.title = post.active_version.title
            post.snippet = post.active_version.snippet
            post.category = post.active_version.category
            post.image = post.active_version.image
            post.comments = Comment.objects.filter(post=post, approved=True).count()
        return posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Blogs"

        # The page middle title based on filtration or search
        if (key := self.kwargs.get("author_id")) is not None:
            context["result_title"] = "Author"
            context["result_value"] = get_object_or_404(Profile, id=key)
        elif (key := self.kwargs.get("cat_id")) is not None:
            context["result_title"] = "Category"
            context["result_value"] = get_object_or_404(Category, id=key)
        elif (key := self.request.GET.get("search")) is not None:
            context["result_title"] = "Search"
            context["result_value"] = key
        return context


class BlogDetail(CreateView):
    """
    The single blog post page for published posts.
    It inherits from CreateView in order to handle comment submitting.
    """

    model = Comment
    fields = ["message"]
    template_name = "blog/blog-single.html"

    def get_success_url(self):
        url = reverse("blog:blog-single", kwargs=self.kwargs)
        return url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = get_object_or_404(
            Post, id=self.kwargs["pk"], status=True, pub_date__lte=now()
        )
        context["title"] = post.active_version.title
        comments = Comment.objects.filter(post=post, approved=True)

        # Adding post's comments grouping by replies os each comment
        for comment in comments:
            if not comment.replied_to:
                comment.replies = comments.filter(replied_to=comment)

        # Adding detail post attributes from it's active version
        post.title = post.active_version.title
        post.content = post.active_version.content
        post.snippet = post.active_version.snippet
        post.category = post.active_version.category
        post.image = post.active_version.image

        context["post"] = post
        context["comments"] = comments
        return context

    def get(self, request, *args, **kwargs):
        """
        get method overridden for counting views.
        """
        post = get_object_or_404(
            Post, id=self.kwargs["pk"], status=True, pub_date__lte=now()
        )
        post.counted_view += 1
        post.save()
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        """
        Handling comment submitting and correspond message
        """
        messages.add_message(
            self.request, messages.SUCCESS, "Your Comment Submitted! Thank you"
        )
        if self.request.user.is_authenticated:
            form.instance.commenter = self.request.user.profile
        else:
            form.instance.name = self.request.POST.get("name")
        form.instance.post = Post.objects.get(id=self.kwargs["pk"])

        if reply := (self.request.POST.get("replied_to_id")):
            form.instance.replied_to = Comment.objects.get(id=reply)

        return super().form_valid(form)


class BlogAuthorList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
    List of posts for each author user. These three permissions are synced by is_author field in model.
    Permissions are handling by a signal in model.
    """

    permission_required = ("blog.add_postversion", "blog.change_post", "blog.add_post")
    template_name = "blog/blog-list.html"
    context_object_name = "posts"
    model = Post
    paginate_by = 9
    extra_context = {"title": "MyPosts", "result_title": "Your Posts"}

    def get_queryset(self):
        posts = Post.objects.filter(author=self.request.user.profile)
        self.extra_context["count"] = len(posts)
        for post in posts:
            post.title = post.active_version.title
            post.snippet = post.active_version.snippet
            post.category = post.active_version.category
            post.image = post.active_version.image
            post.comments = Comment.objects.filter(post=post, approved=True).count()
            post.lastversion = (
                PostVersion.objects.filter(post=post).order_by("-number").first()
            )
            post.pend = True if post.active_version != post.lastversion else False
            post.admin_checked = True if post.lastversion.admin_note else False
        return posts


class BlogAuthor(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    Post creation form for author users with these three permissions (is_author).
    Inherits CreateView to create a new version of a post. Post versions will not update in anyway. In case of
    change request a new version will create for post. New versions dont cause media files duplication.
    It also uses form_class to gain benefit of summernote editor.
    """

    permission_required = ("blog.add_postversion", "blog.change_post", "blog.add_post")
    model = PostVersion
    template_name = "blog/blog-author.html"
    form_class = PostVersionForm
    success_url = reverse_lazy("blog:blog-myposts")

    def form_valid(self, form):
        post_version = form.save()

        # If its change request for an existing post, new version will create by number+1.
        if pk := self.kwargs.get("pk"):
            post = get_object_or_404(Post, id=pk)
            pre_post_version = (
                PostVersion.objects.filter(post=post).order_by("-number").first()
            )
            post_version.number = pre_post_version.number + 1
            post_version.image = pre_post_version.image
            messages.add_message(
                self.request,
                messages.SUCCESS,
                "Your Change request sent successfully. Please wait for admin check, Thank You.",
            )

        # If its a new post creation, first a post create and this post version will be it's active version.
        else:
            messages.add_message(
                self.request,
                messages.SUCCESS,
                "Your new post created successfully. Please wait for admin check, Thank You.",
            )
            post = Post.objects.create(
                author=self.request.user.profile, active_version=post_version
            )
            post_version.number = 1

        # If request contains file for post image it will be replaced
        if image := self.request.FILES.get("image"):
            post_version.image = image

        post_version.post = post
        post_version.author_note = self.request.POST.get("author_note")

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # If its a change request, form will be fulfilled by post's last version.
        if pk := self.kwargs.get("pk"):
            post = get_object_or_404(Post, id=pk, author=self.request.user.profile)
            post_version = (
                PostVersion.objects.filter(post=post).order_by("-number").first()
            )
            title = post_version.title
            snippet = post_version.snippet
            content = post_version.content
            category = post_version.category.all()
            author_note = post_version.author_note
            post.image = post_version.image
            form = PostVersionForm(
                {
                    "title": title,
                    "snippet": snippet,
                    "content": content,
                    "category": category,
                    "author_note": author_note,
                }
            )
            context["title"] = "Edit Post V:%i-->V:%i" % (
                post_version.number,
                post_version.number + 1,
            )
            context["pre_author_note"] = post_version.author_note
            context["form"] = form
            context["admin_note"] = post_version.admin_note
            context["post"] = post
        else:
            context["title"] = "Create New Post"
        return context
