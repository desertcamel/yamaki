from django.conf.urls import include, url
from salesanalytics import views


urlpatterns = [
    url(r'^$', views.SalesAnalyticsHome, name='sales-analytics-home'),
    url(r'^viz$', views.VizHome, name='viz-home'),
]
