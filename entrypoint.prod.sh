#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
  echo "Waiting for postgres to start accepting connections..."

  while ! nc -z "$SQL_HOST" "$SQL_PORT"; do
    sleep 0.1
  done

  echo "Postgres launched..."
fi

echo "Collecting static files"
python manage.py collectstatic --noinput

echo "Applying database migrations"
python manage.py migrate

echo "Starting server"
gunicorn street_food_project.wsgi:application --bind 0.0.0.0:8000

exec "$@"