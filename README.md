# 🐾 CatAndDog — сайт для питомника

Учебно-практический веб-проект на Django для питомника: публикация новостей, управление питомцами и взаимодействие пользователей через комментарии и лайки.  
Проект сочетает классический Django с современными практиками: кеширование, асинхронные задачи, REST API и ролевую модель доступа.

---

## 🚀 Функционал

### 👤 Пользователи
- Регистрация и вход (email/password)
- OAuth-авторизация: Яндекс, ВКонтакте
- Комментирование постов
- Лайки (toggle: 1 пользователь — 1 лайк)
- Просмотр питомцев и новостей

### ✍️ Авторы
- CRUD постов и питомцев
- SEO-дружественные URL (slug)
- Загрузка изображений и видео
- Управление собственным контентом

### 🛠 Администраторы
- Полный контроль над пользователями, постами и питомцами через Django Admin
- REST API с ограничением доступа (`IsAdminUser`)

### ⚡ Производительность
- Кеширование списков и детальных страниц постов
- Автоматическая очистка кеша через Django signals

### 🧵 Фоновые задачи
- Celery + django-celery-beat
- Еженедельная email-рассылка с новыми постами

### 🌐 REST API
- Административный API для управления постами
- Автогенерация документации (Swagger / Redoc)

---

## 🛠 Технологии
- Python 3, Django 5.2
- Django REST Framework
- PostgreSQL, Redis
- Celery, RabbitMQ, django-celery-beat
- django-allauth, django-filter, drf-spectacular
- HTML, CSS
- pytest / pytest-django

---

## ⚙️ Установка и запуск

### 1. Клонируем репозиторий и создаем виртуальное окружение
```bash
git clone https://github.com/username/CatAndDog.git
cd CatAndDog
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```
### 2. Настройка переменных окружения
Локальная разработка (.env.dev)

Создать файл .env.dev в корне проекта:
```
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=postgres://user:password@localhost:5432/dbname
REDIS_URL=redis://localhost:6379/0
EMAIL_HOST=smtp.example.com
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password
```
Docker / Production (.env.docker)

Создать файл .env.docker в корне проекта:
```
SECRET_KEY=your-secret-key
DEBUG=False
DATABASE_URL=postgres://user:password@db:5432/dbname
REDIS_URL=redis://redis:6379/0
EMAIL_HOST=smtp.example.com
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password
```
💡 Примечание: В Docker Compose используются имена сервисов (db, redis) вместо localhost

### 3.Применение миграций и запуск сервера
Локально
```
python manage.py migrate
python manage.py runserver
```
Через Docker
```
docker-compose -f docker-compose.dev.yml up --build
```
### 4. Запуск Celery
Локально
```
# Worker
celery -A CatAndDog worker -l info

# Beat
celery -A CatAndDog beat -l info
```
Через Docker
```
docker-compose -f docker-compose.dev.yml up celery_worker celery_beat
```
### 5. Тестирование
```
pytest
```
```
CatAndDog/
├── CatAndDog/                # Core Django
│   ├── settings/
│   │   ├── base.py
│   │   ├── local.py
│   │   ├── docker.py
│   │   └── production.py
│   ├── celery.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── news/                     # Основное приложение
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── tasks.py
│   ├── signals.py
│   ├── filters.py
│   └── utils/
├── users/                    # Пользователи
├── templates/                # Шаблоны
├── static/                   # Статика
├── nginx/
│   └── default.conf
├── docker-compose.dev.yml
├── docker-compose.prod.yml
├── Dockerfile
├── entrypoint.sh
├── requirements.txt
└── manage.py
```
## 🧪 Цели проекта

Проект создан для практики и демонстрации навыков:

Django CBV: class-based views, миксины, шаблоны
Django REST Framework: ViewSets, permissions, сериализация, OpenAPI
Ролевая модель: Groups, permissions, UserPassesTestMixin, IsAdminUser
Кеширование и оптимизация: Redis, кеширование queryset и detail-view, signals
Фоновые задачи (Celery): асинхронные задачи, celery-beat, email-рассылки
Тестирование: pytest, pytest-django, тесты views, API, cache и permissions