from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Post, Category, Comment
# Register your models here.

class PostAmin(SummernoteModelAdmin):
    summernote_fields = ('content',)
    list_display = ('title','author','counted_view','status','created_date','update_date','id')
    list_filter= ('author','status')

admin.site.register(Post,PostAmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display=('name','id')

admin.site.register(Category,CategoryAdmin)

class CommentAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_date'
    list_filter = ('post',)
    list_display = ('post','commenter','approved','created_date')

admin.site.register(Comment,CommentAdmin)

