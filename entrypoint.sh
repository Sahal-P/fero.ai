#!/bin/bash

python manage.py makemigrations
python manage.py migrate
python manage.py generate_customers_data

python manage.py collectstatic --noinput


exec gunicorn --bind 0.0.0.0:8000 core.wsgi:application
