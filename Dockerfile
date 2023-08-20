# Use an official Python lightweight image
FROM python:3.8-slim

# Set the working directory to /app
WORKDIR /app

# Copy only the requirements file to leverage Docker cache
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . /app/

# Set environment variables
ENV DJANGO_SETTINGS_MODULE=ecommerce_config.settings

# Run the command to start the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
