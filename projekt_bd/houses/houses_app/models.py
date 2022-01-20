from time import timezone
from venv import create
from django.db import models
from django.forms import ModelForm
from django.db.models.signals import post_save, post_init
from time import timezone

class Voivodeship(models.Model):
    name = models.CharField(primary_key=True, max_length=50)

    class Meta:
        db_table = 'voivodeship'

class City(models.Model):
    name = models.CharField(primary_key=True, max_length=50)
    voivodeship = models.ForeignKey('Voivodeship', models.DO_NOTHING, db_column='voivodeship')

    class Meta:
        db_table = 'city'

class Apartment(models.Model):
    address = models.CharField(max_length=255)
    city = models.ForeignKey('City', models.DO_NOTHING, db_column='city')
    floor = models.FloatField()
    id_house = models.FloatField(primary_key=True)
    laitude = models.FloatField()
    longitude = models.FloatField()
    price = models.FloatField()
    rooms = models.FloatField()
    sq = models.FloatField()
    year = models.FloatField()
            
    def __str__(self):
        return str(self.address) + " " + str(self.city.name) + " " + str(self.floor) + " " + str(self.sq) + " " + str(self.price)

    class Meta:
        db_table = 'apartment'

