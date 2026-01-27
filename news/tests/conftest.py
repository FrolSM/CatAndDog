import pytest
from django.contrib.auth.models import User, Group
from news.models import Post, Category

@pytest.fixture
def user(db):
    return User.objects.create_user(username='user', password='12345')

@pytest.fixture
def author(db):
    user = User.objects.create_user(username='author', password='12345')
    group = Group.objects.create(name='authors')
    user.groups.add(group)
    return user

@pytest.fixture
def admin(db):
    return User.objects.create_superuser(
        username='admin',
        password='12345',
        email='admin@test.com'
    )

@pytest.fixture
def category(db):
    return Category.objects.create(name='Test')

@pytest.fixture
def post(db, user, category):
    return Post.objects.create(
        title='Post',
        author=user,
        category=category,
        text='text',
        is_published=True
    )

@pytest.fixture
def draft_post(db, user, category):
    return Post.objects.create(
        title='Draft',
        author=user,
        category=category,
        text='text',
        is_published=False
    )

@pytest.fixture
def auth_client(client, user):
    client.login(username='user', password='12345')
    return client