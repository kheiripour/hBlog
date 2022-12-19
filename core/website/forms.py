
from django import forms
from website.models import Contact
from captcha.fields import CaptchaField,CaptchaTextInput
   
class ContactForm(forms.ModelForm):
    
    captcha  = CaptchaField(widget=CaptchaTextInput(attrs={'class': 'form-control border py-1'}))
    class Meta:
        model = Contact
        fields = ['subject','message']

