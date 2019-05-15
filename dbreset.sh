#!/bin/sh
cd books
rm -d -r migrations/
cd ..
rm -d -r db.sqlite3
python manage.py makemigrations books
python manage.py migrate
python manage.py createsuperuser
