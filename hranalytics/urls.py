from django.conf.urls import include, url
from hranalytics import views


urlpatterns = [
    url(r'^$', views.HRAnalyticsHome, name='hr-analytics-home'),
    url(r'^viz$', views.VizHome, name='viz-home'),
]
