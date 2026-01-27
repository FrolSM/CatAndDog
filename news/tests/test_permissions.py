import pytest
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.core.exceptions import PermissionDenied
from news.models import Post, Category

# ============================================================
# Редактирование поста
# ============================================================

@pytest.mark.django_db
def test_post_update_by_author(client):
    """Автор поста может редактировать свой пост"""
    author = User.objects.create_user(username='author', password='12345')
    category = Category.objects.create(name='Category1')
    post = Post.objects.create(title='Old Title', slug='old-post',
                               author=author, category=category, text='abc', is_published=True)

    client.login(username='author', password='12345')
    url = reverse('post_update', kwargs={'slug': post.slug})
    response = client.post(url, {
        'title': 'Updated Title',
        'text': 'New text',
        'category': category.id,
        'is_published': True
    })

    post.refresh_from_db()
    assert post.title == 'Updated Title'
    # Успешное обновление → редирект
    assert response.status_code == 302


@pytest.mark.django_db
def test_post_update_by_staff(client):
    """Staff может редактировать чужой пост"""
    author = User.objects.create_user(username='author', password='12345')
    staff = User.objects.create_user(username='staff', password='12345', is_staff=True)
    category = Category.objects.create(name='Category1')
    post = Post.objects.create(title='Old Title', slug='old-post',
                               author=author, category=category, text='abc', is_published=True)

    client.login(username='staff', password='12345')
    url = reverse('post_update', kwargs={'slug': post.slug})
    response = client.post(url, {
        'title': 'Staff Update',
        'text': 'Staff text',
        'category': category.id,
        'is_published': True
    })

    post.refresh_from_db()
    assert post.title == 'Staff Update'
    assert response.status_code == 302


@pytest.mark.django_db
def test_post_update_denied_for_anonymous(client):
    """Аноним не может редактировать пост → редирект на login"""
    author = User.objects.create_user(username='author', password='12345')
    category = Category.objects.create(name='Category1')
    post = Post.objects.create(title='Old Title', slug='old-post',
                               author=author, category=category, text='abc', is_published=True)

    url = reverse('post_update', kwargs={'slug': post.slug})
    response = client.get(url)
    # Проверяем редирект на login
    assert response.status_code == 302
    assert '/login/' in response.url


# ============================================================
# Удаление поста
# ============================================================

@pytest.mark.django_db
def test_post_delete_access_by_staff(client):
    """Staff может удалять любой пост"""
    author = User.objects.create_user(username='author', password='12345')
    staff = User.objects.create_user(username='staff', password='12345', is_staff=True)
    category = Category.objects.create(name='Category1')
    post = Post.objects.create(title='Delete Me', slug='delete-post',
                               author=author, category=category, text='abc', is_published=True)

    client.login(username='staff', password='12345')
    url = reverse('post_delete', kwargs={'slug': post.slug})
    response = client.post(url)

    # Пост удалён
    assert not Post.objects.filter(slug='delete-post').exists()
    assert response.status_code == 302


@pytest.mark.django_db
def test_post_delete_access_denied_for_author(client):
    """Автор поста не может удалить пост (только staff)"""
    author = User.objects.create_user(username='author', password='12345')
    category = Category.objects.create(name='Category1')
    post = Post.objects.create(title='Delete Me', slug='delete-me',
                               author=author, category=category, text='abc', is_published=True)

    client.login(username='author', password='12345')
    url = reverse('post_delete', kwargs={'slug': post.slug})

    # Автор не staff → Forbidden (HTTP 403)
    response = client.post(url)
    assert response.status_code == 403

    # Пост должен остаться
    assert Post.objects.filter(slug='delete-me').exists() is True


@pytest.mark.django_db
def test_post_delete_redirect_for_anonymous(client):
    """Анонимный пользователь не может удалять пост → редирект на login"""
    author = User.objects.create_user(username='author', password='12345')
    category = Category.objects.create(name='Category1')
    post = Post.objects.create(title='Delete Me', slug='delete-me',
                               author=author, category=category, text='abc', is_published=True)

    url = reverse('post_delete', kwargs={'slug': post.slug})
    response = client.get(url)

    # Редирект на страницу login
    assert response.status_code == 302
    assert '/login/' in response.url
    # Пост остался
    assert Post.objects.filter(slug='delete-me').exists() is True
