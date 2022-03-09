#!/bin/sh

python3 manage.py migrate
python3 manage.py migrate --database mongodb
python3 manage.py create_superuser
python3 manage.py create_categories
python3 manage.py collectstatic --noinput
sleep 5
python3 manage.py search_index --rebuild -f
python3 manage.py runserver 0.0.0.0:8000
