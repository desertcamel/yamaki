from django.contrib import admin
from .models import Category, BaseCommodity, PurchaseCommodity, TimeSeries
# Register your models here.

admin.site.register(Category)
admin.site.register(BaseCommodity)
admin.site.register(PurchaseCommodity)
admin.site.register(TimeSeries)

