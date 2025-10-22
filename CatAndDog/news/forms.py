from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'Выберите категорию'

    class Meta:
        model = Post
        fields = [
            'title',
            'text',
            'photo',
            'video',
            'category',
        ]
        # имена для полей в форме(но я уже написал в моделях)
        # labels = {
        #     'title': '',
        #     'text': '',
        #     'category': '',
        # }
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 6, })
        }


class CommentForm(forms.ModelForm):
    model = Comment
    fields = ['text']

