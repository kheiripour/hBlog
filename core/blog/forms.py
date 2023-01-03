from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import PostVersion

class PostVersionForm(forms.ModelForm):
    """
    Post version form made to use summernote editor.
    """
    snippet = forms.CharField(widget=forms.Textarea(attrs={"rows":"2"}))
    content = forms.CharField(widget=SummernoteWidget())

    class Meta:
        model = PostVersion
        fields = ['title','snippet','content','category']
