# 🐾 CatAndDog — сайт для питомника

Учебно-практический веб-проект на **Django**, реализующий сайт питомника с новостями, питомцами, системой пользователей, лайками, комментариями и REST API.

Проект создан как тренировочный, но с применением production-подходов: кеширование, фоновые задачи, ролевая модель доступа и автоматические тесты.

---

## 🧩 Описание проекта

Сайт предназначен для публикации новостей питомника и пользовательского контента.  
Зарегистрированные пользователи могут комментировать записи и ставить лайки, а получив роль **автора** — публиковать собственные посты и питомцев.

Проект сочетает **классический Django (CBV + шаблоны)** и **Django REST Framework**.

---

## 🚀 Функциональные возможности

### 👤 Пользователи и авторизация
- регистрация и вход в аккаунт сайта
- OAuth-авторизация:
  - Яндекс
  - ВКонтакте
- разграничение прав доступа:
  - пользователь
  - автор
  - администратор

### 📰 Новости
- публикация и управление постами (CRUD)
- статусы публикации (черновик / опубликовано)
- SEO-дружественные URL (`slug`)
- изображения и видео в постах
- комментарии авторизованных пользователей
- система лайков (1 пользователь — 1 лайк, toggle-логика)

### 🐶 Питомцы
- отдельная страница со списком питомцев
- возможность публикации питомцев пользователями с правами автора

### ⚡ Производительность
- кеширование списка постов с учётом query-параметров
- кеширование детальной страницы поста
- автоматическая очистка кеша через Django signals

### 🧵 Фоновые задачи
- Celery + django-celery-beat
- еженедельная email-рассылка с количеством новых постов

### 🌐 REST API
- административный API для управления постами
- доступ ограничен администраторами (`IsAdminUser`)
- автогенерация документации (Swagger / Redoc)

---

## 🛠 Используемые технологии

- Python 3
- Django 5.2
- Django REST Framework
- PostgreSQL
- Redis
- Celery + RabbitMQ
- django-celery-beat
- django-allauth
- django-filter
- drf-spectacular
- pytest / pytest-django
- HTML / CSS

---

## ⚙️ Установка и запуск

```bash
git clone https://github.com/username/CatAndDog.git
cd CatAndDog
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
Создать файл .env и указать переменные окружения:

env
Копировать код
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=postgres://user:password@localhost:5432/dbname
REDIS_URL=redis://localhost:6379/0
EMAIL_HOST=...
EMAIL_HOST_USER=...
EMAIL_HOST_PASSWORD=...
Применить миграции и запустить сервер:

bash
Копировать код
python manage.py migrate
python manage.py runserver
🧵 Celery
Запуск worker:

bash
Копировать код
celery -A CatAndDog worker -l info
Запуск beat:

bash
Копировать код
celery -A CatAndDog beat -l info
🧪 Тестирование
Проект покрыт тестами:

views и permissions

forms

кеширование

URL routing

REST API

Запуск тестов:

bash
Копировать код
pytest
📌 Структура проекта
text
Копировать код
CatAndDog/
├── CatAndDog/                # core django
│   ├── settings/
│   │   ├── base.py
│   │   ├── local.py
│   │   ├── docker.py
│   │   └── production.py
│   ├── celery.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── news/                     # приложение (основное)
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── tasks.py              # celery 👍
│   ├── signals.py 👍
│   ├── filters.py 👍
│   ├── utils/
│   │   ├── image_converter.py
│   │   ├── video_converter.py
│   │   └── validators.py
│   └── templatetags/
│
├── users/                    # пользователи
├── templates/                # ВСЕ шаблоны
├── static/                   # статика
├── nginx/
│   └── default.conf
├── docker-compose.dev.yml
├── docker-compose.prod.yml
├── Dockerfile
├── entrypoint.sh
├── requirements.txt
├── pytest.ini
├── manage.py
```
## 🧠 Цель проекта

Проект создан для практики и демонстрации следующих навыков:

- 🧩 **Django CBV**  
  Классические class-based views, миксины, шаблоны

- 🌐 **Django REST Framework**  
  ViewSets, permissions, сериализация, OpenAPI

- 👥 **Ролевая модель и права доступа**  
  Groups, permissions, `UserPassesTestMixin`, `IsAdminUser`

- ⚡ **Кеширование и оптимизация**  
  Redis, кеширование queryset и detail-view, signals

- 🧵 **Фоновые задачи (Celery)**  
  Асинхронные задачи, celery-beat, email-рассылки

- 🧪 **Тестирование backend-логики**  
  pytest, pytest-django, тесты views, API, cache и permissions