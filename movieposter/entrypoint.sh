#!/bin/sh

# Остановить выполнение скрипта, если какая-то команда завершится ошибкой
set -e

# Проверка: если мы используем БД в Docker, ждем её готовности
if [ "$DB_HOST" = "db" ]; then
    echo "Ожидание запуска PostgreSQL на $DB_HOST:$DB_PORT..."

    # Проверка доступности порта базы данных через netcat (nc)
    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL запущен и доступен!"
fi

# Автоматическое применение миграций при каждом запуске
echo "Применение миграций базы данных..."
python manage.py migrate

# Запуск сервера Django на всех интерфейсах внутри контейнера
echo "Запуск сервера Django..."
exec python manage.py runserver 0.0.0.0:8000