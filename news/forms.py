from django import forms
from .models import Post, Comment, PostMedia
from django.forms import modelformset_factory



class PostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'Выберите категорию'

    class Meta:
        model = Post
        fields = [
            'title',
            'text',
            'category',
        ]
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 6, })
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


PostMediaFormSet = modelformset_factory(
    PostMedia,
    fields=('media_type', 'file'),
    extra=3,  # сколько полей для загрузки сразу
    can_delete=True
)
