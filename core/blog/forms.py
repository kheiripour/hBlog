from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import PostVersion

class PostVersionForm(forms.ModelForm):
    snippet = forms.CharField(widget=forms.Textarea(attrs={"rows":"2"}))
    content = forms.CharField(widget=SummernoteWidget())
    # author_note = forms.CharField(widget=forms.Textarea(attrs={"rows":"2"}))

    class Meta:
        model = PostVersion
        fields = ['title','snippet','content','category']
