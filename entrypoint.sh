#!/bin/sh

set -e  # падать при любой ошибке

echo "🚀 Starting entrypoint..."

# ----------------------------
# Функция ожидания БД
# ----------------------------
wait_for_db() {
  echo "⏳ Waiting for PostgreSQL at $DB_HOST:$DB_PORT..."

  start_time=$(date +%s)

  while ! nc -z "$DB_HOST" "$DB_PORT"; do
    current_time=$(date +%s)
    elapsed=$((current_time - start_time))

    if [ "$elapsed" -ge "$DB_WAIT_TIMEOUT" ]; then
      echo "❌ ERROR: Could not connect to PostgreSQL within ${DB_WAIT_TIMEOUT}s"
      exit 1
    fi

    echo "⏳ Still waiting... (${elapsed}s)"
    sleep 1
  done

  echo "✅ PostgreSQL is available"
}

# ----------------------------
# Проверка переменных окружения
# ----------------------------
check_env() {
  echo "🔍 Checking required environment variables..."

  required_vars="DB_NAME DB_USER DB_PASSWORD"

  for var in $required_vars; do
    if [ -z "$(eval echo \$$var)" ]; then
      echo "❌ ERROR: $var is not set"
      exit 1
    fi
  done

  echo "✅ Environment variables OK"
}

# ----------------------------
# Django команды
# ----------------------------
run_migrations() {
  echo "📦 Applying migrations..."
  python manage.py migrate --noinput
}

collect_static() {
  echo "🎨 Collecting static files..."
  python manage.py collectstatic --noinput
}

create_superuser() {
  if [ "$CREATE_SUPERUSER" = "true" ]; then
    echo "👤 Creating superuser..."

    python manage.py createsuperuser \
      --noinput || echo "⚠️ Superuser already exists"
  fi
}

# ----------------------------
# Основной сценарий
# ----------------------------
main() {
  check_env
  wait_for_db
  run_migrations
  collect_static
  create_superuser

  echo "🔥 Starting application..."
  exec "$@"
}

main "$@"