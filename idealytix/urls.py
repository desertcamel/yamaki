from django.conf.urls import include, url

from . import views


urlpatterns = [
    url(r'^$', views.bakery_ceo_home, name='bakery-ceo-index'),
    url(r'^portal/$', views.bakery_portal_index, name='bakery-portal-index'),
]

