#!/bin/bash

echo "Build start"

# Install project dependencies
pip install -r requirements.txt

# Collect static files for deployment
python manage.py collectstatic --no-input --clear

echo "Build complete"
