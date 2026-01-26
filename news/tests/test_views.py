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

@pytest.mark.django_db
def test_post_create(client):
    """Проверяем создание поста автором"""
    user = User.objects.create_user(username='author', password='12345')
    group = Group.objects.create(name='authors')
    user.groups.add(group)
    client.login(username='author', password='12345')

    category = Category.objects.create(name='Category1')
    url = reverse('post_create')
    response = client.post(url, {
        'title': 'New Post',
        'text': 'Some text',
        'category': category.id,
        'is_published': True
    })

    post = Post.objects.get(slug='new-post')
    assert post.title == 'New Post'
    assert post.author == user
    assert response.status_code == 302

@pytest.mark.django_db
def test_post_update_by_author(client):
    """Автор может обновлять свой пост"""
    author = User.objects.create_user(username='author', password='12345')
    category = Category.objects.create(name='Category1')
    post = Post.objects.create(title='Old Title', slug='old-post',
                               author=author, category=category, text='abc', is_published=True)

    client.login(username='author', password='12345')
    url = reverse('post_update', kwargs={'slug': post.slug})
    response = client.post(url, {'title': 'Updated Title', 'text': 'New text',
                                 'category': category.id, 'is_published': True})
    post.refresh_from_db()
    assert post.title == 'Updated Title'
    assert response.status_code == 302

@pytest.mark.django_db
def test_post_update_by_staff(client):
    """Staff может обновлять чужой пост"""
    author = User.objects.create_user(username='author', password='12345')
    staff = User.objects.create_user(username='staff', password='12345', is_staff=True)
    category = Category.objects.create(name='Category1')
    post = Post.objects.create(title='Old Title', slug='old-post',
                               author=author, category=category, text='abc', is_published=True)

    client.login(username='staff', password='12345')
    url = reverse('post_update', kwargs={'slug': post.slug})
    response = client.post(url, {'title': 'Staff Update', 'text': 'Staff text',
                                 'category': category.id, 'is_published': True})
    post.refresh_from_db()
    assert post.title == 'Staff Update'
    assert response.status_code == 302

@pytest.mark.django_db
def test_post_delete(client):
    """Проверяем удаление поста staff пользователем"""
    staff = User.objects.create_user(username='staff', password='12345', is_staff=True)
    author = User.objects.create_user(username='author', password='12345')
    category = Category.objects.create(name='Category1')
    post = Post.objects.create(title='To Delete', slug='delete-post',
                               author=author, category=category, text='abc', is_published=True)

    client.login(username='staff', password='12345')
    url = reverse('post_delete', kwargs={'slug': post.slug})
    response = client.post(url)
    assert not Post.objects.filter(slug='delete-post').exists()
    assert response.status_code == 302

@pytest.mark.django_db
def test_post_comment(client):
    """Проверяем создание комментария авторизованным пользователем"""
    user = User.objects.create_user(username='commenter', password='12345')
    author = User.objects.create_user(username='author', password='12345')
    category = Category.objects.create(name='Category1')
    post = Post.objects.create(title='Comment Post', slug='comment-post',
                               author=author, category=category, text='abc', is_published=True)

    client.login(username='commenter', password='12345')
    url = reverse('post_comment', kwargs={'slug': post.slug})
    response = client.post(url, {'text': 'Nice post!'})
    assert Comment.objects.filter(post=post, user=user).exists()
    assert response.status_code == 302

@pytest.mark.django_db
def test_like_post_toggle(client):
    """Проверяем установку и снятие лайка (toggle)"""
    user = User.objects.create_user(username='liker', password='12345')
    author = User.objects.create_user(username='author', password='12345')
    category = Category.objects.create(name='Category1')
    post = Post.objects.create(title='Like Post', slug='like-post',
                               author=author, category=category, text='abc', is_published=True)

    client.login(username='liker', password='12345')
    url = reverse('like_post', kwargs={'slug': post.slug})

    # Ставим лайк
    response = client.post(url)
    assert response.json()['liked'] is True
    assert post.like_count() == 1

    # Убираем лайк
    response = client.post(url)
    assert response.json()['liked'] is False
    assert post.like_count() == 0
