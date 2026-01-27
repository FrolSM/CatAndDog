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
