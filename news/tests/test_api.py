import pytest
from rest_framework.test import APIClient
from django.urls import reverse

@pytest.mark.django_db
def test_post_viewset_admin_only(admin, user):
    """
        Проверяем, что доступ к списку постов через DRF ViewSet
        разрешён только администраторам (IsAdminUser).

        Обычный аутентифицированный пользователь должен получать 403,
        администратор — 200 OK.
        """
    client = APIClient()
    url = reverse('post-list')

    # обычный пользователь → запрещено
    client.force_authenticate(user=user)
    response = client.get(url)
    assert response.status_code == 403

    # админ → разрешено
    client.force_authenticate(user=admin)
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_post_create_admin_only(admin, user, category):
    """
    Проверяем, что создание поста через API
    доступно только администратору.

    POST-запрос от обычного пользователя → 403 Forbidden
    POST-запрос от администратора → 201 Created
    """
    client = APIClient()
    url = reverse('post-list')

    data = {
        'title': 'API post',
        'text': 'API text',
        'category': category.id,
        'is_published': True,
    }

    # обычный пользователь → запрещено
    client.force_authenticate(user=user)
    assert client.post(url, data).status_code == 403

    # админ → разрешено
    client.force_authenticate(user=admin)
    assert client.post(url, data).status_code == 201