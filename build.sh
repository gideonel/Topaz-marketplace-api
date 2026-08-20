#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static assets
python manage.py collectstatic --noinput

# Run database migrations

python manage.py makemigrations

python manage.py migrate
