from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import Post,Category

class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=100)
    snippet = forms.CharField(widget=forms.Textarea(attrs={"rows":"2"}))
    content = forms.CharField(widget=SummernoteWidget())
    categories = forms.ModelMultipleChoiceField(queryset= Category.objects.all())
    author_note = forms.CharField(widget=forms.Textarea(attrs={"rows":"2"}))

    class Meta:
        model = Post
        fields = ['author']
