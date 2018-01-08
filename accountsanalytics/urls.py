from django.conf.urls import include, url
from accountsanalytics import views


urlpatterns = [
    url(r'^$', views.AccountsAnalyticsHome, name='accounts-analytics-home'),
    url(r'^viz$', views.VizHome, name='viz-home'),
]
