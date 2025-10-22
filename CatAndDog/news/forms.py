from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'text',
            'photo',
            'video',
            'category',
        ]


class CommentForm(forms.ModelForm):
    model = Comment
    fields = ['text']

