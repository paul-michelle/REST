#!/bin/sh

echo "Waiting for databases to start accepting connections..."
while ! nc -z "$SQL_HOST" "$SQL_PORT"; do
  sleep 0.33
done
echo "Databases launched..."

echo "Collecting static files"
python manage.py collectstatic --noinput

echo "Updating database"
python manage.py makemigrations street_food_app
python manage.py migrate --noinput

echo "Creating a superuser"
echo "from django.contrib.auth import get_user_model;\
  User = get_user_model();\
  User.objects.create_superuser('$ADMIN_NAME','$ADMIN_EMAIL', '$ADMIN_PASSWORD')" |
  python manage.py shell

exec "$@"