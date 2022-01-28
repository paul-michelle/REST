#!/bin/sh

echo "Waiting for database to start accepting connections..."
while ! nc -z "$SQL_HOST" "$SQL_PORT"; do
  sleep 0.1
done
echo "Databases launched..."

echo "Collecting static files"
python manage.py collectstatic --noinput

echo "Updating database"
python manage.py makemigrations street_food_app
python manage.py migrate --noinput


create_superuser () {
  echo "from django.contrib.auth import get_user_model;\
  User = get_user_model();\
  User.objects.create_superuser('$1','$2', '$3')" |
  python manage.py shell
}

echo "Creating a superuser... Wait a sec..."
if create_superuser "$ADMIN_NAME" "$ADMIN_EMAIL" "$ADMIN_PASSWORD" 2>/dev/null; then
   echo "Superuser successfully."
else
   echo "Superuser with the creds given already exists."
fi

exec "$@"
