#!/bin/bash
# Install dependencies from the correct directory
pip install -r pixel_cost_optimizer/requirements.txt --break-system-packages

# Go into the project directory
cd pixel_cost_optimizer

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate
