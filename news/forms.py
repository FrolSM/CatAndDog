from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'Выберите категорию'
        # self.fields['title'].validators = [RussianValidator(), ]

    class Meta:
        model = Post
        fields = [
            'title',
            'text',
            'photo',
            'video',
            'category',
        ]

        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 6, })
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
