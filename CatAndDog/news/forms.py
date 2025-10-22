from django.forms import ModelForm
from .models import Post, Comment


class PostForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
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


class CommentForm(ModelForm):
    model = Comment
    fields = ['text']

