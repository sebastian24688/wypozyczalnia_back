#!/bin/bash

sleep 5s
echo "Odpalam entrypoint"
python manage.py makemigrations zarzadzanie_pojazdami
python manage.py migrate

python manage.py loaddata zarzadzanie_pojazdami/sample_data/pojazd.json
python manage.py loaddata zarzadzanie_pojazdami/sample_data/klient.json
python manage.py loaddata zarzadzanie_pojazdami/sample_data/wypozyczenie.json
python manage.py loaddata zarzadzanie_pojazdami/sample_data/grupy.json

python manage.py runserver 0.0.0.0:8000
