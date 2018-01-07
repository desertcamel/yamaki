from django.conf.urls import include, url
from salesanalytics import views


urlpatterns = [
    url(r'^$', views.SalesAnalyticsHome, name='sales-analytics-home'),
]
