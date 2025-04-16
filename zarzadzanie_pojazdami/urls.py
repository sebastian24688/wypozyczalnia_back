from django.urls import path
from .views import DodajPojazd, WyszukiwarkaPojazdow, WylistujMarki, WylistujKategorie, EdytujPojazd, UsunPojazd, \
    Wyloguj, \
    WypozyczPojazd, WyszukajWypozyczenia, WypozyczeniaKlienta, CzyZalogowany, RejestracjaKlienta, \
    EdytujStatusWypozyczenia, UsunWypozyczenie, JakaGrupa, Oplac

urlpatterns = [
    path('dodaj_pojazd/', DodajPojazd.as_view(), name='dodaj_pojazd'),
    # curl -X POST -H "Content-Type: application/json" -d "{\"marka\": \"Audi\", \"model\": \"RS6\", \"rok_produkcji\": 2022}" http://127.0.0.1:8000/zarzadzanie_pojazdami/api/dodaj_pojazd/
    # Audi
    # R8
    # 2019
    # 2400
    # 570
    # 3.1
    # 5.2
    # 87500
    path('wyszukaj_pojazdy/', WyszukiwarkaPojazdow.as_view(), name='wyszukaj_pojazdy'),
    # http://127.0.0.1:8000/zarzadzanie_pojazdami/wyszukaj_pojazdy/?kategoria=sportowy&marka=Audi
    path('wylistuj_marki/', WylistujMarki.as_view(), name='wylistuj_marki'),
    path('wylistuj_kategorie/', WylistujKategorie.as_view(), name='wylistuj_kategorie'),
    path('edytuj_pojazd/<str:nr_rejestracyjny>/', EdytujPojazd.as_view(), name='edytuj-pojazd'),
    # curl -X PATCH http://localhost:8000/zarzadzanie_pojazdami/edytuj_pojazd/numer_rejestracyjny/ -H "Authorization: Bearer <TOKEN>" -d '{
    #   "cena": 55000.00
    # }'
    path('usun_pojazd/<str:nr_rejestracyjny>/', UsunPojazd.as_view(), name='usun_pojazd'),
    # curl -X DELETE -H "Authorization: Token ff1d26b07137060406d37f00ad48045a79361002" http://127.0.0.1:8000/zarzadzanie_pojazdami/usun_pojazd/WL9309T/
    # curl -X DELETE http://127.0.0.1:8000/zarzadzanie_pojazdami/usun_pojazd/WL9309T/
    path('wypozycz_pojazd/', WypozyczPojazd.as_view(), name='wypozycz_pojazd'),
    # curl -X POST -H "Content-Type: application/json" -H "Authorization: Token 756842c8f8ae20411579be446c970faa502af17f" -d '{"pojazd": 3,"data_wypozyczenia": "2024-01-01", "ilosc_dni": 5}' http://192.168.8.148:8000/zarzadzanie_pojazdami/wypozycz_pojazd/
    path('wyszukaj_wypozyczenia/', WyszukajWypozyczenia.as_view(), name='wyszukaj_wypozyczenia'),
    # http://localhost:8000/zarzadzanie_pojazdami/wyszukaj_wypozyczenia/?email=k2@example.com
    # http://localhost:8000/zarzadzanie_pojazdami/wyszukaj_wypozyczenia/
    path('wypozyczenia_klienta/', WypozyczeniaKlienta.as_view(), name='wypozyczenia_klienta'),
    path('edytuj_status_wypozyczenia/<int:id>/', EdytujStatusWypozyczenia.as_view(), name='edytuj_status_wypozyczenia'),
    # curl -X PUT -H "Content-Type: application/json" -d '{"status_wypozyczenia": "Wypożyczony"}' http://localhost:8000/zarzadzanie_pojazdami/edytuj_status_wypozyczenia/1/
    path('usun_wypozyczenie/<int:pk>/', UsunWypozyczenie.as_view(), name='usun_wypozyczenie'),
    #curl -X DELETE -H "Authorization: Token 756842c8f8ae20411579be446c970faa502af17f" http://localhost:8000/zarzadzanie_pojazdami/usun_wypozyczenie/8/
    path('oplac/<int:pk>/', Oplac.as_view(), name='oplac'),


    # autoryzacja
    # login
    # curl -X POST -H "Content-Type: application/json" -d "{\"username\": \"klient1\", \"password\": \"passpasspass\"}" http://192.168.8.148:8000/login/
    # curl -X POST -H "Content-Type: application/json" -d '{"username": "klient1", "password": "passpasspass"}' http://192.168.8.148:8000/login/
    path('wyloguj/', Wyloguj.as_view(), name='wyloguj'),
    # curl -X POST -H "Authorization: Token ff1d26b07137060406d37f00ad48045a79361002" http://127.0.0.1:8000/wyloguj/
    path('rejestracja/', RejestracjaKlienta.as_view(), name='rejestracja_klienta'),
    path('czy_zalogowany/', CzyZalogowany.as_view(), name='wyszukaj_wypozyczenia'),
    path('jaka_grupa/', JakaGrupa.as_view(), name='jaka_grupa'),
]

# hasła użytkowników
# passpasspass