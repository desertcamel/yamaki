from django.contrib import admin
from .models import Category, BaseCommodity, PurchaseCommodity
# Register your models here.

admin.site.register(Category)
admin.site.register(BaseCommodity)
admin.site.register(PurchaseCommodity)


