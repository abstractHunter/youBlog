from django.contrib import admin
from .models import Post, Tag, Comment

# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status', 'created_at')
    list_filter = ("status",)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Comment)
