
from django.urls import reverse_lazy
from django.views.generic import TemplateView,CreateView
from captcha.helpers import captcha_image_url
from .models import Slider,Contact
from .forms import ContactForm
# Create your views here.

class IndexView(TemplateView):
    template_name = "website/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slides = Slider.objects.filter(is_active=True)
        for slide in  slides:
            slide.post.image = slide.post.active_version.image
            slide.post.title = slide.post.active_version.title
            slide.post.snippet = slide.post.active_version.snippet
        context['slides'] = slides
        context['title'] = "Home"
        return context


class ContactView(CreateView):
    template_name = "website/conatct.html"
    model = Contact
    form_class = ContactForm
    success_url = reverse_lazy('website:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Contact"
        return context

    def form_valid(self, form):
        
        if self.request.user.is_authenticated:
            form.instance.sender = self.request.user.profile
            form.instance.name = self.request.user.profile
            form.instance.email = self.request.user.email
        else:
            form.instance.name = self.request.POST.get('name')
            form.instance.email = self.request.POST.get('email')

        return super().form_valid(form)








