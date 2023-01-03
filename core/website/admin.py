from django.contrib import admin
from .models import Slider, Contact, Newsletter

# Register your models here.


class SliderAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "post", "snippet", "image", "is_active")


admin.site.register(Slider, SliderAdmin)


class ContactAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "sender",
        "subject",
        "message",
        "created_date",
        "admin_note",
        "is_done",
    )


admin.site.register(Contact, ContactAdmin)


class NewsletterAdmin(admin.ModelAdmin):
    list_display = ("email",)


admin.site.register(Newsletter, NewsletterAdmin)
