#!/bin/sh
source venv/bin/activate
exec gunicorn -w 12 -b :5000 --access-logfile - --error-logfile - app:app
