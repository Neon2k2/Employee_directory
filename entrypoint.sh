#!/bin/sh

python manage.py migrate

python manage.py shell <<EOF
from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser(
        username="admin",
        email="admin@example.com",
        password="admin123"
    )
    print("Superuser created")
else:
    print("Superuser already exists")
EOF

python manage.py collectstatic --noinput

gunicorn Employee_details.wsgi:application --bind 0.0.0.0:$PORT
