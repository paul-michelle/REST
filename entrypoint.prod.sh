#!/bin/sh

echo "Waiting for databases to start accepting connections..."
while ! nc -z "$SQL_HOST" "$SQL_PORT"; do
  sleep 0.1
done
echo "Databases launched..."

echo "Collecting static files"
python manage.py collectstatic --noinput

echo "Updating database"
python manage.py makemigrations authentication
python manage.py makemigrations street_food_app
python manage.py migrate --noinput

create_superuser() {
  echo "from django.contrib.auth import get_user_model;\
  User = get_user_model();\
  User.objects.create_superuser(username='$1', email='$2', password='$3')" |
    python manage.py shell
}

echo "Creating a superuser..."
if create_superuser "$ADMIN_NAME" "$ADMIN_EMAIL" "$ADMIN_PASSWORD" 2>/dev/null; then
  echo "Superuser successfully created."
else
  echo "Superuser with the creds given already exists."
fi

exec "$@"
