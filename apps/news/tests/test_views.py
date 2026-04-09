import io
from PIL import Image
import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.contrib.auth.models import User, Group
from apps.news.models import Post, Comment, Like, Category, PostMedia

def get_test_image():
    file = io.BytesIO()
    image = Image.new('RGB', (100, 100), color='red')
    image.save(file, 'JPEG')
    file.seek(0)
    return SimpleUploadedFile(
        'test.jpg',
        file.read(),
        content_type='image/jpeg'
    )

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
    assert Comment.objects.filter(post=post, author_comm=user).exists()
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

@pytest.mark.django_db
def test_get_like_count(client):
    """Проверяем корректность подсчета лайков"""
    user = User.objects.create_user(username='liker', password='12345')
    author = User.objects.create_user(username='author', password='12345')
    category = Category.objects.create(name='Category1')
    post = Post.objects.create(title='Like Count', slug='like-count',
                               author=author, category=category, text='abc', is_published=True)
    Like.objects.create(user=user, post=post)

    url = reverse('get_like_count', kwargs={'slug': post.slug})
    response = client.get(url)
    assert response.json()['count'] == 1

@pytest.mark.django_db
def test_create_post_with_media_form(author, client, category):
    # логинимся как автор
    client.login(username='author', password='12345')

    url = reverse('post_create')

    # создаем тестовые файлы
    image_file = get_test_image()
    video_file = SimpleUploadedFile("test.mp4", b"video_content", content_type="video/mp4")

    data = {
        'title': 'Test Post Form',
        'text': 'This is a test post',
        'category': category.id,
        'form-TOTAL_FORMS': '2',
        'form-INITIAL_FORMS': '0',
        'form-MIN_NUM_FORMS': '0',
        'form-MAX_NUM_FORMS': '3',
        'form-0-media_type': 'photo',
        'form-0-file': image_file,
        'form-1-media_type': 'video',
        'form-1-file': video_file,
    }

    response = client.post(url, data, follow=True)
    assert response.status_code == 200

    post = Post.objects.get(title='Test Post Form')
    assert post.media.count() == 2
    assert post.has_photo is True
    assert post.has_video is True

@pytest.mark.django_db
def test_create_post_with_media_api(admin, client, category):
    client.login(username='admin', password='12345')

    url = reverse('post-list')  # DRF ViewSet, замените на правильный URL, если роутинг другой

    image_file = get_test_image()
    video_file = SimpleUploadedFile("test_api.mp4", b"video_content", content_type="video/mp4")

    data = {
        'title': 'API Post',
        'text': 'Post via API',
        'category': category.id,
        'is_published': True,
        'photos': [image_file],
        'videos': [video_file]
    }

    response = client.post(url, data, format='multipart')
    assert response.status_code == 201

    post = Post.objects.get(title='API Post')
    assert post.media.count() == 2
    assert post.has_photo is True
    assert post.has_video is True

@pytest.mark.django_db
def test_update_post_add_and_delete_media(author, client, category):
    client.login(username='author', password='12345')

    # Создаем пост без медиа
    post = Post.objects.create(
        title='Update Test Post',
        author=author,
        category=category,
        text='Original text',
        is_published=True
    )

    url = reverse('post_update', kwargs={'slug': post.slug})

    # Создаем тестовые файлы
    image_file = get_test_image()
    video_file = SimpleUploadedFile("update.mp4", b"video_content", content_type="video/mp4")

    # Изначально добавим один медиафайл
    existing_media = PostMedia.objects.create(
        post=post,
        media_type='photo',
        file=image_file
    )

    # Данные формы для UpdateView
    data = {
        'title': 'Update Test Post',
        'text': 'Updated text',
        'category': category.id,
        # formset management fields
        'form-TOTAL_FORMS': '2',
        'form-INITIAL_FORMS': '1',  # один уже существует
        'form-MIN_NUM_FORMS': '0',
        'form-MAX_NUM_FORMS': '3',
        # первый медиа (существующий) пометим на удаление
        'form-0-id': existing_media.id,
        'form-0-media_type': existing_media.media_type,
        'form-0-DELETE': 'on',
        # второй медиа — новый файл
        'form-1-media_type': 'video',
        'form-1-file': video_file,
    }

    response = client.post(url, data, follow=True)
    assert response.status_code == 200

    post.refresh_from_db()

    # Проверяем, что старый медиа удален, новый добавлен
    media = post.media.all()
    assert media.count() == 1
    assert media.first().media_type == 'video'
