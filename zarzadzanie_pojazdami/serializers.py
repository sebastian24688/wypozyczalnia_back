from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Pojazd, Wypozyczenie
from django.core.validators import MaxLengthValidator, MinLengthValidator, MaxValueValidator, MinValueValidator
from datetime import datetime


class PojazdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pojazd
        fields = '__all__'

    marka = serializers.CharField(
        validators=[
            MinLengthValidator(limit_value=1, message='Nazwa marki nie może być pusta.'),
            MaxLengthValidator(limit_value=20, message='Nazwa marki nie może przekraczać 20 znaków.'),
        ])

    model = serializers.CharField(
        validators=[
            MinLengthValidator(limit_value=1, message='Nazwa modelu nie może być pusta.'),
            MaxLengthValidator(limit_value=20, message='Nazwa modelu nie może przekraczać 20 znaków.'),
        ])

    rok_produkcji = serializers.IntegerField(
        validators=[
            MinValueValidator(limit_value=1900, message='Rok produkcji nie może być wcześniejszy niż 1900.'),
            MaxValueValidator(limit_value=datetime.now().year,
                              message='Rok produkcji nie może być późniejszy niż obecny rok.'),
        ])

    cena = serializers.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(limit_value=0, message='Cena nie może być ujemna.')])

    moc = serializers.IntegerField(
        validators=[
            MinValueValidator(limit_value=1, message='Moc nie może być mniejsza niż 1.'),
            MaxValueValidator(limit_value=2000, message='Moc nie może być większa niż 2000.'),
        ])

    przyspieszenie = serializers.DecimalField(
        max_digits=4, decimal_places=1,
        validators=[
            MinValueValidator(limit_value=1.0, message='Przyspieszenie nie może być mniejsza niż 1.0.'),
        ])

    pojemnosc = serializers.DecimalField(
        max_digits=4, decimal_places=1,
        validators=[
            MinValueValidator(limit_value=0.1, message='Pojemność nie może być mniejsza niż 0.1.'),
            MaxValueValidator(limit_value=7.0, message='Pojemność nie może być większa niż 7.0.'),
        ])

    przebieg = serializers.IntegerField(
        validators=[
            MinValueValidator(limit_value=1, message='Przebieg nie może być mniejszy niż 1.'),
            MaxValueValidator(limit_value=1000000, message='Przebieg nie może być większy niż 1000000.'),
        ])


class ObrazekSerializer(serializers.Serializer):
    obrazek = serializers.ImageField()


class WypozyczenieSerializer(serializers.ModelSerializer):
    klient_imie = serializers.ReadOnlyField(source='klient.first_name')
    klient_nazwisko = serializers.ReadOnlyField(source='klient.last_name')
    email = serializers.ReadOnlyField(source='klient.email')
    pojazd_marka = serializers.ReadOnlyField(source='pojazd.marka')
    pojazd_model = serializers.ReadOnlyField(source='pojazd.model')
    pojazd_numer_rejestracyjny = serializers.ReadOnlyField(source='pojazd.nr_rejestracyjny')

    class Meta:
        model = Wypozyczenie
        fields = ['klient_imie', 'klient_nazwisko', 'email', 'pojazd_marka', 'pojazd_model', 'pojazd_numer_rejestracyjny',
                  'data_wypozyczenia', 'ilosc_dni', 'status_wypozyczenia', 'czy_oplacone']


class WypozyczenieUsunSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wypozyczenie
        fields = '__all__'


class WypozyczenieKlientaSerializer(serializers.ModelSerializer):
    pojazd_marka = serializers.ReadOnlyField(source='pojazd.marka')
    pojazd_model = serializers.ReadOnlyField(source='pojazd.model')

    class Meta:
        model = Wypozyczenie
        fields = ['pojazd_marka', 'pojazd_model', 'data_wypozyczenia', 'ilosc_dni', 'status_wypozyczenia',
                  'czy_oplacone']


class RejestracjaKlientaSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        return user

class EdytujStatusWypozyczeniaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wypozyczenie
        fields = ['status_wypozyczenia']

