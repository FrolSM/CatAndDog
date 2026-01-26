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

@pytest.mark.django_db
def test_post_detail_view(client):
    """Проверяем детальную страницу поста и обработку 404"""
    user = User.objects.create_user(username='author', password='12345')
    category = Category.objects.create(name='News')
    post = Post.objects.create(title='Test Post', slug='test-post',
                               author=user, category=category, text='abc', is_published=True)

    # Существующий пост
    url = reverse('post_detail', kwargs={'slug': post.slug})
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['post'] == post

    # Несуществующий пост
    url = reverse('post_detail', kwargs={'slug': 'nonexistent'})
    response = client.get(url)
    assert response.status_code == 404