from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.urls import reverse_lazy
import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import Category, Commodity, APISource, TimeSeries

import logging
logger = logging.getLogger(__name__)

# Create your views here.


def home(request):
    logger.debug('#### LOGGER #### DISPLAY HOME PAGE#######')
    return render( request, 'home.html',)

def PurchasingIndexView(request):
    return render( request, 'CommodityTracker/purchasing_index_home.html',)

def index(request):
    return render( request, 'CommodityTracker/commodity_index.html',)


def CommodityBenchmarkView(request, base_pk, bench_pk):
    return render( request, 'CommodityTracker/commodity_benchmark.html',)


# Company
@method_decorator(login_required, name='dispatch')
class CommodityListView(generic.ListView):
    model = Category
    template_name = 'CommodityTracker/commodity_list.html'

    def get_queryset(self):
        return Category.objects.all().order_by('name')

@method_decorator(login_required, name='dispatch')
class CategoryDetailView(generic.DetailView):
    model = Category

@method_decorator(login_required, name='dispatch')
class CategoryCreateView(generic.CreateView):
    model = Category
    success_url = reverse_lazy('commodities-list')
    template_name = 'CommodityTracker/category_create.html'
    fields = '__all__'



@method_decorator(login_required, name='dispatch')
class CommodityCreateView(generic.DetailView):
    model = Commodity



# Commodity
import json
import quandl
import pandas as pd
import gviz_api
from datetime import datetime
from datetime import date
import quandl


def download_quandl_data(commodity):

    logger.log ("## DEBUG ##### INSIDE DOWNLOAD QUAND DATA ..........1")
    quandl.ApiConfig.api_key = commodity.api_key

    dfset = quandl.Dataset(commodity.api_code)
    logger.log ("## DEBUG ##### INSIDE DOWNLOAD QUAND DATA ..........2")

    data = dfset.data()

    # Store in database
    df = data.to_pandas()
    print ("####### INSIDE DOWNLOAD QUAND DATA ..........3")
    try:
        for index, row in df.iterrows():
            ts = TimeSeries(commodity=commodity, date = index, value=row['Value'])
            ts.save()
            print ('created')
    except Exception as e: 
        print (e)
    print ("####### INSIDE DOWNLOAD QUAND DATA ..........4")

    return


@login_required
def CommodityDetailView(request, pk):
    template = 'CommodityTracker/commodity_detail.html'
    commodity = Commodity.objects.get(pk=pk)
    print (commodity)

    # Check if the last date of commodity is in past. If so, update records for missing days
    needs_udpate = True

    if needs_udpate:  # download missing data and update the database 
        try:
            download_quandl_data (commodity)
        except :
            print ('connection error. Showing date until last update')
    
    # Fetch from database
    ts_queryset = TimeSeries.objects.filter(commodity=commodity)
    # Convert to json
    l = []
    for ts in ts_queryset:
        a = [ts.date, ts.value]
        l.append (a)
    
    lod = ([{'date': datetime.combine(d, datetime.min.time()), 'value': v} for d, v in l])

    # Loading it into gviz_api.DataTable
    desc = {'date': ('datetime', 'Date'), 'value': ('number', 'Value')}
    data_table = gviz_api.DataTable(desc)
    data_table.LoadData(lod)

    # Creating a JSon string
    json_output = data_table.ToJSon(columns_order=("date", "value"),
                            order_by="date")


    context = {'dataset': json_output}
    # Render the HTML template index.html with the data in the context variable.
    return render(request, template, context)



# SUGGESTIONS
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView

class SignUpView(CreateView):
    template_name = 'CommodityTracker/signup.html'
    form_class = UserCreationForm


from django.contrib.auth.models import User
from django.http import JsonResponse

def validate_username(request):
    print ('##### ENTER THE VIEW FUNCTION ########')
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'A user with this username already exists.'
    return JsonResponse(data)