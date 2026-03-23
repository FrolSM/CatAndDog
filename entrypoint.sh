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
