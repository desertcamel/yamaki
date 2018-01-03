from django.contrib import admin
from .models import Category, Commodity, APISource, TimeSeries
# Register your models here.

admin.site.register(Category)
admin.site.register(Commodity)
admin.site.register(APISource)
admin.site.register(TimeSeries)

