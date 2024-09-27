#!/bin/bash

# Выполняем миграции
python manage.py migrate --no-input

# Проверяем переменные окружения и создаем суперпользователя
if [ -z "$DJANGO_SUPERUSER_USERNAME" ] || [ -z "$DJANGO_SUPERUSER_EMAIL" ] || [ -z "$DJANGO_SUPERUSER_PASSWORD" ]; then
  echo "Отсутствуют необходимые переменные окружения для создания суперпользователя:"
  echo "DJANGO_SUPERUSER_USERNAME: $DJANGO_SUPERUSER_USERNAME"
  echo "DJANGO_SUPERUSER_EMAIL: $DJANGO_SUPERUSER_EMAIL"
  echo "DJANGO_SUPERUSER_PASSWORD: (скрыто)"
else
  echo "Создание суперпользователя..."
  python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists():
    User.objects.create_superuser(
        '$DJANGO_SUPERUSER_USERNAME',
        '$DJANGO_SUPERUSER_EMAIL',
        '$DJANGO_SUPERUSER_PASSWORD'
    )
  "
fi

# Запускаем сервер
exec python manage.py runserver 0.0.0.0:8000