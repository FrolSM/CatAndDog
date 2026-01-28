import pytest
from django.core.cache import cache
from django.urls import reverse
from news.models import Post

@pytest.mark.django_db
def test_post_detail_is_cached(client, post):
    cache.clear()
    cache_key = f'post-{post.slug}'

    # до запроса кеш пуст
    assert cache.get(cache_key) is None

    url = reverse('post_detail', kwargs={'slug': post.slug})

    response1 = client.get(url)
    assert response1.status_code == 200

    # после запроса объект появился в кеше
    cached_post = cache.get(cache_key)
    assert cached_post is not None
    assert cached_post.id == post.id

    # второй запрос — тоже 200 (из кеша или БД — неважно)
    response2 = client.get(url)
    assert response2.status_code == 200

@pytest.mark.django_db
def test_cache_cleared_on_post_save(post):
    cache_key = f'post-{post.slug}'
    cache.set(cache_key, post)

    # меняем поле, которое не влияет на slug
    post.text = 'new text'
    post.save()

    assert cache.get(cache_key) is None