from django.db import models
from datetime import datetime, date
from django.contrib.auth.models import User, AbstractUser


class Pojazd(models.Model):
    KATEGORIA_CHOICES = [
        ('suv', 'SUV'),
        ('osobowy', 'Osobowy'),
        ('sportowy', 'Sportowy'),
    ]

    SKRZYNIA_CHOICES = [
        ('automatyczna', 'Automatyczna'),
        ('manualna', 'Manualna'),
    ]

    NAPED_CHOICES = [
        ('przod', 'Przód'),
        ('tyl', 'Tył'),
        ('4x4', '4x4'),
    ]

    nr_rejestracyjny = models.CharField(max_length=8, unique=True)
    marka = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    rok_produkcji = models.IntegerField()
    cena = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=True)
    kategoria = models.CharField(max_length=20, choices=KATEGORIA_CHOICES)
    moc = models.IntegerField()
    opis = models.TextField()
    skrzynia = models.CharField(max_length=20, choices=SKRZYNIA_CHOICES)
    naped = models.CharField(max_length=10, choices=NAPED_CHOICES)
    przyspieszenie = models.DecimalField(max_digits=4, decimal_places=1)
    pojemnosc = models.DecimalField(max_digits=4, decimal_places=1, blank=False, null=True)
    przebieg = models.IntegerField()
    zdjecie1 = models.ImageField(upload_to='img/')
    zdjecie2 = models.ImageField(upload_to='img/')
    zdjecie3 = models.ImageField(upload_to='img/')
    zdjecie4 = models.ImageField(upload_to='img/')
    zdjecie5 = models.ImageField(upload_to='img/')


class Wypozyczenie(models.Model):
    REZERWACJA = 'Rezerwacja'
    WYPOZYCZENIE = 'Wypożyczenie'
    ZAKONCZONY = 'Zakończony'

    STATUS_CHOICES = [
        (REZERWACJA, 'Rezerwacja'),
        (WYPOZYCZENIE, 'Wypożyczony'),
        (ZAKONCZONY, 'Zakończone'),
    ]

    klient = models.ForeignKey(User, on_delete=models.CASCADE)
    pojazd = models.ForeignKey(Pojazd, on_delete=models.CASCADE)
    data_wypozyczenia = models.DateField(blank=False, null=True)
    ilosc_dni = models.IntegerField(default=1)
    status_wypozyczenia = models.CharField(max_length=50, choices=STATUS_CHOICES,  default='Rezerwacja')
    czy_oplacone = models.BooleanField(default=False)
