from django.shortcuts import render

import logging
logger = logging.getLogger(__name__)

# Create your views here.

def home(request):
    logger.debug('#### LOGGER #### DISPLAY HOME PAGE#######')
    return render( request, 'idealytix/bakery_ceo_home.html',)

def bakery_portal_index(request):
    return render( request, 'idealytix/bakery_portal_index.html',)

def sales_analytics_home(request):
    return render(request, 'idealytix/sales_analytics_index.html',)

def web_analytics_home(request):
    return render(request, 'idealytix/web_analytics_index.html',)

def customer_analytics_home(request):
    return render(request, 'idealytix/customer_analytics_index.html',)

def inventory_analytics_home(request):
    return render(request, 'idealytix/inventory_analytics_index.html',)

def commodity_analytics_home(request):
    return render(request, 'idealytix/commodity_analytics_index.html',)
    
def accounts_analytics_home(request):
    return render(request, 'idealytix/accounts_analytics_index.html',)

