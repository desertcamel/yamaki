from django.db import models
import json
import quandl
import pandas as pd
from datetime import datetime
from datetime import date
from django.core.validators import MinValueValidator, MaxValueValidator

class Category (models.Model):
    name = models.CharField(max_length=25)
    description = models.TextField(max_length=1000, null = False)

    def get_commodity_count(self):
        count = self.basecommodities.count()
        return count

    def __str__(self):
        return self.name

class BaseCommodity(models.Model):
    name = models.CharField(max_length=25, null=False)
    description = models.TextField(max_length=1000, null = False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='basecommodities')

    # API Details
    api_source = models.CharField(max_length=50)
    api_key = models.CharField(max_length=25)
    api_version = models.CharField(max_length=25, blank=True)
    api_code = models.CharField(max_length=20)

    #
    last_updated = models.DateTimeField(default=date(2000, 1, 1))

    def needs_update(self):
        time_since_last_update = date.today() - self.last_updated.date()
        if time_since_last_update.days > 5 :
            print ('commodity data needs update')
            return True
        else:
            print ('commodity data does not need update')
            return False

    def update_data(self):
        if (self.api_source == 'Quandl'):
            quandl.ApiConfig.api_key = self.api_key
            dfset = quandl.Dataset(self.api_code, start_date=str(self.last_updated), end_date=str(date.today()))
            data = dfset.data()
            entries = data.to_pandas()

            print ('INSIDE UPDATE DATA')
#            print ('ENTRIES>>>>>>>>>>')
#            print (entries)

            try:
                for index, row in entries.iterrows():
                    ts = TimeSeries()
                    ts.is_base_commodity = True
                    ts.base_commodity = self
                    ts.is_purchase_commodity = False
                    ts.purchase_commodity = None
                    ts.date = index
                    ts.value = row['Value']
                    
                    ts.save()
#                    print (ts)
            except Exception as e:
                print ("Error in making TimeSeries entry:")
                print (e) 

            self.last_updated = date.today()
            return True # Updated

        return False # Not updated




    def __str__(self):
        return self.name


# Purchase Commodity
class PurchaseCommodity(models.Model):
    name = models.CharField(max_length=25, null=False)
    description = models.TextField(max_length=1000, null = False)
    company_name = models.CharField(max_length=50)
    #
    last_updated = models.DateTimeField()

    # Benchmark Information
    weight1 = models.FloatField(null=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(100)]) # values between 0 to 1
    weight2 = models.FloatField(null=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    weight3 = models.FloatField(null=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    benchmark1 = models.ForeignKey(BaseCommodity, on_delete=models.SET_NULL, null=True, related_name='benchmark_1')
    benchmark2 = models.ForeignKey(BaseCommodity, on_delete=models.SET_NULL, null=True, related_name='benchmark_2')
    benchmark3 = models.ForeignKey(BaseCommodity, on_delete=models.SET_NULL, null=True, related_name='benchmark_3')

    def update_values(self, entries):
        for entry in entries:
            ts = TimeSeries.objects.get_or_create(
                is_base_commodity = False,
                base_commodity = None,
                is_purchase_commodity = True,
                purchase_commodity = self,
                date = entry['date'],
                value = entry['value']
                )

    def __str__(self):
        return self.name

# Data Records
class TimeSeries(models.Model):
    is_base_commodity = models.BooleanField(default=False)
    base_commodity = models.ForeignKey(BaseCommodity, on_delete=models.SET_NULL, 
                                        null=True, related_name='records'
                                        )

    is_purchase_commodity = models.BooleanField(default=False)
    purchase_commodity = models.ForeignKey(PurchaseCommodity, on_delete=models.SET_NULL, 
                                            null=True, related_name='records'
                                        )

    date = models.DateTimeField()
    value = models.FloatField()

    