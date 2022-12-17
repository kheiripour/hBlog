from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Slider
# Create your views here.

class IndexView(TemplateView):
    template_name = "website/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slides = Slider.objects.filter(is_active=True)
        context['slides'] = slides
        context['title'] = "Home"
        return context


