from django.conf.urls import include, url
from webanalytics import views


urlpatterns = [
    url(r'^$', views.WebAnalyticsHome, name='web-analytics-home'),
    url(r'^viz$', views.VizHome, name='viz-home'),
]
