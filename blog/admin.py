from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Post, Comment

# Register your models here.


class PostAdmin(SummernoteModelAdmin):
    list_display = ('title', 'slug', 'published', 'created_at', 'thumbnail')
    list_filter = ("published",)
    search_fields = ['title', 'content']
    summernote_fields = ('content',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'content')


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
