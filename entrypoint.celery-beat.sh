echo "Waiting for Gunicorn to start handling requests..."
while ! nc -z web 8000; do
  sleep 0.1
done
echo "Gunicorn's ready"

celery -A street_food_project beat -l info