#!/bin/sh

if [ "$DATABASE" = "postgres" ]; then
  echo "Waiting for postgres to start accepting connections..."

  while ! nc -z "$SQL_HOST" "$SQL_PORT"; do
    sleep 0.1
  done

  echo "Postgres launched..."
fi

echo "Collecting static files"
python manage.py collectstatic --noinput

echo "Updating database"
python manage.py makemigrations
python manage.py migrate --noinput


echo "Creating a superuser"
echo "from django.contrib.auth import get_user_model;\
  User = get_user_model();\
  User.objects.create_superuser('whoami','who@m.i', 'whoami')" |
  python manage.py shell

echo "Starting server"
gunicorn street_food_project.wsgi:application --bind 0.0.0.0:8000

exec "$@"
