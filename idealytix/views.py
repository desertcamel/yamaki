from django.shortcuts import render

import logging
logger = logging.getLogger(__name__)

# Create your views here.

def home(request):
    logger.debug('#### LOGGER #### DISPLAY HOME PAGE#######')
    return render( request, 'idealytix/bakery_ceo_home.html',)

def bakery_portal_index(request):
    return render( request, 'idealytix/bakery_portal_index.html',)

