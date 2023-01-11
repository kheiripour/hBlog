from django import forms
from website.models import Contact
from captcha.fields import CaptchaField, CaptchaTextInput


class ContactForm(forms.ModelForm):

    captcha = CaptchaField(
        widget=CaptchaTextInput(attrs={"class": "form-control border py-1"})
    )
    name = forms.CharField(
        max_length=100,
        label="Name*",
        required=False,
        widget=forms.TextInput(attrs={"class": "border"}),
    )
    email = forms.EmailField(
        required=False,
        label="Email*",
        widget=forms.TextInput(attrs={"class": "border"}),
    )
    subject = forms.CharField(
        max_length=250, widget=forms.TextInput(attrs={"class": "border"})
    )
    message = forms.CharField(
        max_length=250, widget=forms.Textarea(attrs={"class": "border"})
    )

    class Meta:
        model = Contact
        fields = ["subject", "message", "name", "email"]

    def is_valid(self) -> bool:
        profile_id = self.data.get("sender_id", None)
        valid = True
        if profile_id is None:
            if self.data.get("name") == "":
                self.add_error(field="name", error="Name is required")
                valid = False
            if self.data.get("email") == "":
                self.add_error(field="email", error="Email is required")
                valid = False
        if valid:
            return super().is_valid()
        return False
