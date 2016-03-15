#!/bin/sh

/env/bin/python3 /app/manage.py migrate --noinput
/env/bin/python3 /app/manage.py runserver 0.0.0.0:8080  --noreload