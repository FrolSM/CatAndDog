from django_filters import FilterSet, ModelChoiceFilter, CharFilter
from .models import Post, Users


class PostFilter(FilterSet):
    # author = ModelChoiceFilter(queryset=Users.objects.all(), label='Автор', empty_label='Все авторы')
    # title = CharFilter(label='Заголовок', lookup_expr='iregex')
    # text = CharFilter(label='Содержание поста', lookup_expr='iregex')
    # category =
    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'text': ['icontains'],
            'category': ['exact'],
        }
