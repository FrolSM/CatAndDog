import pytest
from django.urls import reverse, resolve
from news.views import (
    PostsList,
    PostDetail,
    PostCreate,
    PostUpdate,
    PostDelete,
    ContactsView,
    PetsList,
    RulesCreatingPostView,
    like_post,
    get_like_count,
)


# ============================================================
# resolve() tests
# Проверяем:
# 1) что URL существует
# 2) что он привязан к нужному view
# Эти тесты НЕ выполняют view, а только проверяют роутинг
# ============================================================


@pytest.mark.django_db
def test_post_list_resolves():
    # Главная страница должна вести на PostsList
    resolver = resolve('/')
    assert resolver.func.view_class == PostsList


@pytest.mark.django_db
def test_post_detail_resolves(post):
    # Детальная страница поста должна резолвиться по slug
    resolver = resolve(f'/post/{post.slug}/')
    assert resolver.func.view_class == PostDetail


@pytest.mark.django_db
def test_post_create_resolves():
    # URL создания поста должен быть связан с PostCreate
    resolver = resolve('/post/create/')
    assert resolver.func.view_class == PostCreate


@pytest.mark.django_db
def test_post_update_resolves(post):
    # URL редактирования поста должен вести на PostUpdate
    resolver = resolve(f'/post/{post.slug}/update/')
    assert resolver.func.view_class == PostUpdate


@pytest.mark.django_db
def test_post_delete_resolves(post):
    # URL удаления поста должен вести на PostDelete
    resolver = resolve(f'/post/{post.slug}/delete/')
    assert resolver.func.view_class == PostDelete


@pytest.mark.django_db
def test_contacts_resolves():
    # Страница контактов — обычный TemplateView
    resolver = resolve('/contacts/')
    assert resolver.func.view_class == ContactsView


@pytest.mark.django_db
def test_pets_resolves():
    # Страница со списком питомцев
    resolver = resolve('/pets/')
    assert resolver.func.view_class == PetsList


@pytest.mark.django_db
def test_rules_resolves():
    # Страница с правилами создания постов
    resolver = resolve('/rules_creating_post/')
    assert resolver.func.view_class == RulesCreatingPostView


@pytest.mark.django_db
def test_like_post_resolves(post):
    # AJAX endpoint для лайка поста (function-based view)
    resolver = resolve(f'/post/{post.slug}/like/')
    assert resolver.func == like_post


@pytest.mark.django_db
def test_get_like_count_resolves(post):
    # AJAX endpoint для получения количества лайков
    resolver = resolve(f'/post/{post.slug}/count/')
    assert resolver.func == get_like_count

# ============================================================
# reverse() + HTTP status tests
# Проверяем:
# 1) что URL можно построить по name
# 2) что страница реально открывается
# ============================================================

@pytest.mark.parametrize('url_name', [
    'post_list',
    'contacts',
    'pets_list',
    'rules_creating_post',
])
@pytest.mark.django_db
def test_public_pages_open(client, url_name):
    # Публичные страницы должны быть доступны анониму (HTTP 200)
    response = client.get(reverse(url_name))
    assert response.status_code == 200


@pytest.mark.django_db
def test_post_detail_open(client, post):
    # Детальная страница опубликованного поста должна открываться
    response = client.get(
        reverse('post_detail', kwargs={'slug': post.slug})
    )
    assert response.status_code == 200


@pytest.mark.parametrize('url_name', [
    'post_create',
])
@pytest.mark.django_db
def test_protected_pages_redirect_for_anonymous(client, url_name):
    # Защищённые страницы должны редиректить анонимного пользователя
    # (LoginRequiredMixin / UserPassesTestMixin)
    response = client.get(reverse(url_name))
    assert response.status_code == 302


# ============================================================
# Дополнительные полезные тесты
# ============================================================

@pytest.mark.django_db
def test_nonexistent_url_returns_404(client):
    # Проверяем, что несуществующий URL возвращает 404
    response = client.get('/this-url-does-not-exist/')
    assert response.status_code == 404


@pytest.mark.django_db
def test_like_post_method_not_allowed(client, post):
    # Проверяем, что GET на like_post возвращает 405 (только POST разрешен)
    url = reverse('like_post', kwargs={'slug': post.slug})
    response = client.get(url)
    assert response.status_code == 405


@pytest.mark.django_db
@pytest.mark.parametrize('url_name', [
    'post_update',
    'post_delete',
    'post_comment',
])
def test_all_protected_pages_redirect_for_anonymous(client, post, url_name):
    # Проверяем все защищенные страницы: редиректят анонимов на login
    url = reverse(url_name, kwargs={'slug': post.slug})
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_reverse_post_detail(post):
    # Проверка, что reverse с slug формирует правильный URL
    url = reverse('post_detail', kwargs={'slug': post.slug})
    assert url == f'/post/{post.slug}/'


@pytest.mark.django_db
def test_get_like_count_returns_json(client, post):
    # Проверяем, что AJAX endpoint get_like_count возвращает JSON с ключом 'count'
    url = reverse('get_like_count', kwargs={'slug': post.slug})
    response = client.get(url)
    assert response.status_code == 200
    json_data = response.json()
    assert 'count' in json_data