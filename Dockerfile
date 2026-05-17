FROM python:3.11-slim

WORKDIR /app

# Install build tools
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Environment
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Railway sets $PORT automatically
EXPOSE $PORT

# Run migrations, collect static, then start Gunicorn
CMD ["sh", "-c", "python manage.py migrate && python manage.py shell -c \"from django.contrib.auth import get_user_model; User=get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin','admin@example.com','admin123')\" && python manage.py collectstatic --noinput && gunicorn Employee_details.wsgi:application --bind 0.0.0.0:$PORT"]
