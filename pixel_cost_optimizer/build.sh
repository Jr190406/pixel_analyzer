#!/bin/bash
# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Run migrations (Optional: Ensure database is up to date)
python manage.py migrate
