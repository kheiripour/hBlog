from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.shortcuts import render
from datetime import datetime
from django.contrib import messages
from .models import Slider, Contact, Newsletter
from .forms import ContactForm

# Create your views here.


def handler404_view(request, exception):
    response = render(request=request, template_name="404.html", status=404)
    return response


class IndexView(CreateView):
    template_name = "website/index.html"
    model = Newsletter
    fields = ["email"]
    success_url = reverse_lazy("website:index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slides = Slider.objects.filter(
            is_active=True, post__status=True, post__pub_date__lte=datetime.now()
        ).order_by("order")
        for slide in slides:
            slide.post.image = slide.post.active_version.image
            slide.post.title = slide.post.active_version.title
            slide.post.snippet = slide.post.active_version.snippet
        context["slides"] = slides
        context["title"] = "Home"
        return context

    def form_valid(self, form):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            "Your email for newsletter recieved successfully, Thank You.",
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(
            self.request,
            messages.ERROR,
            "Your email has problem for newsletter, please check.",
        )
        return super().form_invalid(form)


class ContactView(CreateView):
    template_name = "website/conatct.html"
    model = Contact
    form_class = ContactForm
    success_url = reverse_lazy("website:index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Contact"
        return context

    def form_valid(self, form):

        if self.request.user.is_authenticated:
            form.instance.sender = self.request.user.profile
            form.instance.name = self.request.user.profile
            form.instance.email = self.request.user.email
        else:
            form.instance.name = self.request.POST.get("name")
            form.instance.email = self.request.POST.get("email")
        messages.add_message(
            self.request,
            messages.SUCCESS,
            "Your message recieved successfully, Thank You.",
        )
        return super().form_valid(form)
