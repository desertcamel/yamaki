"""crmsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import RedirectView

from idealytix import views as idealytix_views
from CommodityTracker import views as commodity_views
from boards import views as boards_views

#URL pattern mappings

urlpatterns = [
    url(r'^$', idealytix_views.home, name='home'),
]

urlpatterns += [
    url(r'^commodity/', include('CommodityTracker.urls')),
    url(r'^forums/', include('boards.urls')),    
    url(r'^accounts/', include('accounts.urls')),    
    url(r'^bakery/', include('idealytix.urls')),
]

#Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    url(r'^accounts/', include('django.contrib.auth.urls')),
]

urlpatterns += [
    url(r'^admin/', admin.site.urls),
]


