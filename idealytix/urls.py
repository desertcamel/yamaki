from django.conf.urls import include, url

from . import views


urlpatterns = [
    url(r'^$', views.bakery_portal_index, name='home'),
]
