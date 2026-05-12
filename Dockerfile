FROM python:3.11.1-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBUG=False
ENV SECRET_KEY=temp-build-key-only

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "Employee_details.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]
