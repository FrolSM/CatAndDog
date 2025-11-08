from django_filters import FilterSet, ModelChoiceFilter, CharFilter
from .models import Post, Category


class PostFilter(FilterSet):
    title = CharFilter(label='Заголовок', lookup_expr='iregex')
    text = CharFilter(label='Содержание поста', lookup_expr='iregex')
    category = ModelChoiceFilter(queryset=Category.objects.all(), label='Категории', empty_label='Все категории')

    # class Meta:
    #     model = Post
    #     fields = {
    #         'title': ['icontains'],
    #         'text': ['icontains'],
    #         'category': ['exact'],
    #     }
