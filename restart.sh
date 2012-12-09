#!/bin/sh

rm ../arcnet.db
rm templates/netimg/profiles/*

python manage.py syncdb --noinput
python test.py
python manage.py runserver
