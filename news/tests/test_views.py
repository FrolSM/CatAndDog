import pytest
from django.urls import reverse
from django.contrib.auth.models import User, Group
from news.models import Post, Comment, Like, Category

@pytest.mark.django_db
def test_posts_list_view(client):
    """Проверяем, что список постов отображается корректно"""
    url = reverse('post_list')
    response = client.get(url)
    assert response.status_code == 200
    assert 'posts' in response.context
