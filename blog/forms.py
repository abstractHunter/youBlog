from django.forms import ModelForm

from .models import Comment, Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'published', 'tags', 'thumbnail']


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
