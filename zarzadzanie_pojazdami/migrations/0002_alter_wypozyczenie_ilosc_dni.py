# Generated by Django 3.2.23 on 2024-01-28 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zarzadzanie_pojazdami', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wypozyczenie',
            name='ilosc_dni',
            field=models.IntegerField(default=1),
        ),
    ]
