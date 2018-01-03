from django.db import models
from datetime import date

# Create your models here.

class Category (models.Model):
    name = models.CharField(max_length=25)
    def __str__(self):
        return self.name


class APISource (models.Model):
    API_SOURCES = (
        ('Quandl', 'Quandl'),
        ('Reuters', 'Reuters'),
        ('IndexMundi', 'IndexMundi'),
    )
    name = models.CharField(max_length=25, choices=API_SOURCES)

    def __str__(self):
        return self.name


class Commodity(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    COMMODITY_CHOICES = (
        ('Sunflower Oil', 'Sunflower Oil'),
        ('Palm Oil', 'Palm Oil'),
        ('Olive Oil', 'Olive Oil'),
    )    
    name = models.CharField(choices=COMMODITY_CHOICES, max_length=25)
    summary = models.TextField(max_length=1000)

    api_source = models.ForeignKey(APISource, on_delete=models.SET_NULL, null=True)
    api_key = models.CharField(max_length=25)
    api_version = models.CharField(max_length=25, blank=True)
    api_code = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class TimeSeries(models.Model):
    commodity = models.ForeignKey(Commodity, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField()
    value = models.FloatField()

