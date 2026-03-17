# 1. Базовый образ
FROM python:3.12-slim

# 2. Переменные окружения
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 3. Рабочая директория
WORKDIR /app

# 4. Системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 5. Установка зависимостей отдельно (кэш Docker)
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 6. Копируем проект
COPY . .

# 7. Создаём пользователя (без root)
RUN useradd -m appuser
USER appuser

# 8. Порт
EXPOSE 8000

# 9. Запуск
CMD ["gunicorn", "CatAndDog.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]