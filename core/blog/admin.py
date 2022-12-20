from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Post,PostVersion, Category, Comment
# Register your models here.

class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0
class PostVersionInline(admin.TabularInline):
    model = PostVersion
    extra = 0

class PostAdmin(admin.ModelAdmin):
    
    list_display = ('active_version','author','counted_view','status','created_date','update_date','id')
    list_filter= ('author','status')
    inlines = [
        PostVersionInline,
        CommentInline,
    ]
    # changing active version queryset to limit choice in post versions: 
    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['active_version'].queryset = PostVersion.objects.filter(post=context['object_id'])
        return super(PostAdmin, self).render_change_form(request, context, *args, **kwargs)

admin.site.register(Post,PostAdmin)
class CategoryAdmin(admin.ModelAdmin):
    list_display=('name','id')

admin.site.register(Category,CategoryAdmin)


@admin.action(description='Approve selected comments')
def make_approved(modeladmin, request, queryset):
    queryset.update(approved=True)
class CommentAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_date'
    list_filter = ('post',)
    list_display = ('id','post','commenter','approved','replied_to','created_date')
    actions = [make_approved]

    # changing replied_to queryset to limit choice in post comments: 
    def render_change_form(self, request, context, *args, **kwargs):
        obj = Comment.objects.get(id=context['object_id'])
        context['adminform'].form.fields['replied_to'].queryset = Comment.objects.filter(post=obj.post,replied_to=None).exclude(id=obj.id)
        return super(CommentAdmin, self).render_change_form(request, context, *args, **kwargs)
    


admin.site.register(Comment,CommentAdmin)

class PostVersionAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)
    list_display = ('post','number','title','created_date','update_date','id')

admin.site.register(PostVersion,PostVersionAdmin)
