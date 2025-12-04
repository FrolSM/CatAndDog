from django import forms
from django.core.exceptions import ValidationError

from .models import Post, Comment
from django.utils.deconstruct import deconstructible


# @deconstructible
# class RussianValidator:
#     ALLOWED_CHARS = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя0123456789- '
#     code = 'russian'
#
#     def __init__(self, message=None):
#         self.message = message if message else 'Должны присутствовать только русские символы, цифры, дефис и пробел.'
#
#     def __call__(self, value, *args, **kwargs):
#         if not (set(value) <= set(self.ALLOWED_CHARS)):
#             raise ValidationError(self.message, code=self.code)


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

    # def clean(self):
    #     title = self.cleaned_data.get('title')
    #     ALLOWED_CHARS = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя0123456789- '
    #
    #     if not (set(title) <= set(ALLOWED_CHARS)):
    #         raise ValidationError('Должны присутствовать только русские символы, цифры, дефис и пробел.')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
