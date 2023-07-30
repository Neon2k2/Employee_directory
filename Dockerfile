# Use an official Python runtime as the base image
FROM python:3.11.1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file and install the Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Expose the port the Django application will run on
EXPOSE 8000

# Set the command to start the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
