#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt
pip install gunicorn uvicorn
pip freeze > requirements.txt
python3 manage.py collectstatic --no-input
python3 manage.py makemigrations
python3 manage.py migrate
