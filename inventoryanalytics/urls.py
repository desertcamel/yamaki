from django.conf.urls import include, url
from inventoryanalytics import views


urlpatterns = [
    url(r'^$', views.InventoryAnalyticsHome, name='inventory-analytics-home'),
]
