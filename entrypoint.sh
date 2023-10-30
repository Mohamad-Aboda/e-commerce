#!/bin/sh

# Apply migrations
python manage.py migrate

# Create new migration files
python manage.py makemigrations

# Start the Django development server
python manage.py runserver 0.0.0.0:8000

