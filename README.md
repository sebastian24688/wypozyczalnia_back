pip install django

# utworzenie aplikacji
django-admin startproject nauka
cd .\nauka\
python .\manage.py startapp aplikacja

# tworzenie bazy danych
python manage.py makemigrations aplikacja
python .\manage.py migrate
docker-compose exec django python manage.py makemigrations zarzadzanie_pojazdami
docker-compose exec django python manage.py migrate

docker-compose exec django python manage.py loaddata zarzadzanie_pojazdami/sample_data/pojazd.json
docker-compose exec django python manage.py loaddata zarzadzanie_pojazdami/sample_data/klient.json
docker-compose exec django python manage.py loaddata zarzadzanie_pojazdami/sample_data/wypozyczenie.json
docker-compose exec django python manage.py loaddata zarzadzanie_pojazdami/sample_data/grupy.json


# użytkownycy
python .manage.py createsuperuser

# uruchamianie serwera
python  .\manage.py runserver

# obsługa bazy
python.exe .\manage.py shell
from aplikacja.models import Idea
obj = Idea.objects.all()
obj[1].title

# Postgresql
docker build -t rentcardb .
docker run -p 5432:5432 --name rentcardb -d rentcardb

# pg-admin
docker run -p 5051:80 -e PGADMIN_DEFAULT_EMAIL=user@example.com -e PGADMIN_DEFAULT_PASSWORD=pass --name pgadmin-container -d dpage/pgadmin4


curl -X DELETE -H "Authorization: Token 756842c8f8ae20411579be446c970faa502af17f" http://localhost:8000/zarzadzanie_pojazdami/usun_wypozyczenie/8/

