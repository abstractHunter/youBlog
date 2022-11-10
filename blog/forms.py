from django import forms
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from django_summernote.fields import SummernoteTextField

from .models import Comment, Post


class PostForm(forms.ModelForm):
    content = SummernoteTextField()

    class Meta:
        model = Post
        fields = ['title', 'published', 'content', 'tags', 'thumbnail']
        """ widgets = {
            'content': SummernoteWidget(),
        } """


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
