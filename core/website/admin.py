from django.contrib import admin
from .models import Slider
# Register your models here.

class SliderAdmin(admin.ModelAdmin):
    list_display=('id','post','snippet','image','is_active')

admin.site.register(Slider,SliderAdmin)


