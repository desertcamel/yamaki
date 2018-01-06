from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.generic.edit import View, CreateView, UpdateView, DeleteView
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.urls import reverse_lazy
import datetime
from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import Category, BaseCommodity, PurchaseCommodity, TimeSeries
from CommodityTracker.forms import PurchaseCommodityForm

import logging
logger = logging.getLogger(__name__)

# Commodity
import json
import quandl
import pandas as pd
import gviz_api
from datetime import datetime
from datetime import date
# Create your views here.


def home(request):
    logger.debug('#### LOGGER #### DISPLAY HOME PAGE#######')
    return render( request, 'home.html',)

def PurchasingIndexView(request):
    return render( request, 'CommodityTracker/purchasing_home.html',)

def index(request):
    return render( request, 'CommodityTracker/commodity_index.html',)


def CommodityBenchmarkView(request, base_pk, bench_pk):
    return render( request, 'CommodityTracker/commodity_benchmark.html',)


# Company
class CommodityListView(generic.ListView):
    model = Category
    template_name = 'CommodityTracker/commodity_list.html'

    def get_queryset(self):
        return Category.objects.all().order_by('name')

class CategoryListView(generic.ListView):
    model = Category
    template_name = 'CommodityTracker/category_list.html'

    def get_queryset(self):
        return Category.objects.all().order_by('name')

class BaseCommodityListView(generic.ListView):
    model = BaseCommodity
    template_name = 'CommodityTracker/basecommodity_list.html'

    def get_queryset(self):
        return BaseCommodity.objects.all().order_by('name')

class PurchaseCommodityListView(generic.ListView):
    model = PurchaseCommodity
    template_name = 'CommodityTracker/purchasecommodity_list.html'

    def get_queryset(self):
        return PurchaseCommodity.objects.all().order_by('name')

class TimeSeriesListView(generic.ListView):
    model = TimeSeries
    template_name = 'CommodityTracker/timeseries_list.html'

    def get_queryset(self):
        return TimeSeries.objects.all()

class CategoryDetailView(generic.DetailView):
    model = Category


class _PurchaseCommodityDetailView(generic.DetailView):
    model = PurchaseCommodity
    template = 'CommodityTracker/commodity_benchmark.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['purchasecommodity_list'] = PurchaseCommodity.objects.all()
        context['dataset'] = _purchase_commodity_util(self)
        return context






class TimeSeriesDetailView(generic.DetailView):
    model = TimeSeries

class CategoryCreateView(generic.CreateView):
    model = Category
    success_url = reverse_lazy('commodities-list')
    template_name = 'CommodityTracker/category_create.html'
    fields = '__all__'



class CommodityCreateView(generic.DetailView):
    model = BaseCommodity






def BaseCommodityDetailView(request, pk):
    template = 'CommodityTracker/commodity_detail.html'
    base_commodity = BaseCommodity.objects.get(pk=pk)
    print (base_commodity)

    # if required, update the dataset
    if base_commodity.needs_update():
        status = base_commodity.update_data()
        print ("Update status: " + status)


    # Fetch from database
    ts_queryset = TimeSeries.objects.filter(base_commodity=base_commodity)
    # Convert to json
    l = []
    for ts in ts_queryset:
        l.append ([ts.date, ts.value])
    
    lod = ([{'date': datetime.combine(date, datetime.min.time()), 'value': value} for date, value in l])

    # Loading it into gviz_api.DataTable
    desc = {'date': ('datetime', 'Date'), 'value': ('number', 'Value')}
    data_table = gviz_api.DataTable(desc)
    data_table.LoadData(lod)

    # Creating a JSon string
    json_output = data_table.ToJSon(columns_order=("date", "value"),
                            order_by="date")


    context = {'basecommodity': base_commodity  , 'dataset': json_output}
    # Render the HTML template index.html with the data in the context variable.
    return render(request, template, context)























"""
Admin accessible init functions

"""

def app_init(request):
    # CREATE BASIC MODELS AND INSTANTIATE WITH VALUES


    base_commodity_list = [
        ['Vegetable Oil','Rapeseed Oil','ODA/PROIL_USD'],
        ['Vegetable Oil','Sunflower Oil','ODA/PSUNO_USD'],
        ['Vegetable Oil','Olive Oil','ODA/POLVOIL_USD'],
        ['Vegetable Oil','Palm Oil','ODA/PPOIL_USD'],
        ['Agriculture Softs','Cocoa beans','ODA/PCOCO_USD'],
        ['Agriculture Softs','Tea','ODA/PTEA_USD'],
        ['Agriculture Softs','US Imports Sugar','ODA/PSUGAUSA_USD'],
        ]

    for row in base_commodity_list:
        new_cat, c = Category.objects.get_or_create(name=row[0], description='Agro Commodities')

        new_base_commodity, c = BaseCommodity.objects.get_or_create( name = row[1],
                                                            description = row[1],
                                                            category = new_cat,
                                                            api_source = 'Quandl',
                                                            api_key = 'UyAuo5henNjLfxt-ahsS',
                                                            api_version = '',
                                                            api_code = row[2],
                                                            last_updated = date.today()
                                                            )

        new_base_commodity.update_data()
    print ('udpate completed')

    return render( request, 'CommodityTracker/test_page.html',)


import numpy as np
def get_dummy_benchmark_index(request):
    # GET BENCHMARK 1
    periods_1 = 12 * 7
    bench_dates1 = pd.date_range('20100101', periods=periods_1, freq='M')
    bench1 = pd.DataFrame(np.random.randint(size=periods_1, low=99, high=201), index=bench_dates1, columns=['values'])
    bench1=bench1.sort_index(axis=0, ascending=True)
    bench1.columns = ['bench1']
    weight1 = 0.7
    bench1 = bench1 * weight1

    # GET BENCHMARK 2
    periods_2 = 12 * 7
    bench_dates2 = pd.date_range('20100101', periods=periods_2, freq='M')
    bench2 = pd.DataFrame(np.random.randint(size=periods_2, low=199, high=501), index=bench_dates2, columns=['values'])
    bench2=bench2.sort_index(axis=0, ascending=True)
    bench2.columns = ['bench2']
    weight2 = 0.3
    bench2 = bench2 * weight2

    # ALIGN THE INDEXES OF BENCHMARKS
    if bench1.index[0] < bench2.index[0]:
        bench1 = bench1[bench2.index[0]:]
    else:
        bench2 = bench2[bench1.index[0]:]

    # BRING IN A SINGLE TABLE. BACKFILL EMPTY VALUES
    bench_comb = pd.concat([bench1, bench2], axis=1)
    bench_comb = bench_comb.fillna(method='ffill')

    # CREATE COMPOSITE BENCHMARK COLUMN BY MAKING WEIGHTED ADDITION
    bench_comb ['bench'] = bench_comb['bench1'] + bench_comb['bench2']

    # GENERATE PURCHASE DATA
    periods_3 = 2 * 7
    purch_dates = pd.date_range('20100101', periods=periods_3, freq='6M')
    purchase_data = pd.DataFrame(np.random.randint(size=periods_3, low=999, high=3001), index=purch_dates, columns=['purchases'])

    if bench_comb.index[0] < purchase_data.index[0]:
        bench_comb = bench_comb[purchase_data.index[0]:]
    else:
        purchase_data = purchase_data[bench_comb.index[0]:]

        
    index_comb = pd.concat([purchase_data, bench_comb['bench']], axis=1)
    index_comb = index_comb.fillna(method='ffill')

    # BASE BENCHMARK TO THE PURCHASE COMMODITY
    factor = index_comb['purchases'][0] / index_comb['bench'][0] 
    index_comb['bench'] = index_comb['bench'] * factor
#    index_comb = index_comb.round(1)

    # CONVERT TO JSON
    l = []
    for index, value in index_comb.iterrows():
        l.append ([index, value['purchases'], value['bench']])
    
    lod = ([{'date': datetime.combine(date, datetime.min.time()), 'purchase': purchase, 'benchmark': benchmark} for date, purchase, benchmark in l])

    # Load it into gviz_api.DataTable
    desc = {'date': ('datetime', 'Date'), 
            'purchase': ('number', 'Purchase'), 
            'benchmark': ('number', 'Benchmark')
            }
    data_table = gviz_api.DataTable(desc)
    data_table.LoadData(lod)

    # Create a JSon string
    json_output = data_table.ToJSon(
                            columns_order=("date", "purchase", 'benchmark'),
                            order_by="date"
                            )

    # Prepare the return function
    template = 'CommodityTracker/benchmark.html'
    context = {'dataset': json_output}
    return render(request, template, context)




def purchase_commodity_form(request):
    template = 'CommodityTracker/purchase_commodity_form.html'

    if request.method == 'POST':
        form = PurchaseCommodityForm(request.POST, request.FILES)

        if form.is_valid():
            purchase_commodity = PurchaseCommodity(name = form.cleaned_data['name'],
                                                    description = form.cleaned_data['description'], 
                                                    company_name = form.cleaned_data['company_name'],
                                                    last_updated = date.today(),
                                                    weight1 = form.cleaned_data['weight1'],
                                                    weight2 = form.cleaned_data['weight2'],
                                                    weight3 = form.cleaned_data['weight3'],
                                                    benchmark1 = form.cleaned_data['benchmark1'],
                                                    benchmark2 = form.cleaned_data['benchmark2'],
                                                    benchmark3 = form.cleaned_data['benchmark3'],
        )
            purchase_commodity.save()
            process_data(request.FILES['commodity_purchase_data'], purchase_commodity)
            json_output = Prepare_DataFrame(purchase_commodity, form.cleaned_data['weight1'], form.cleaned_data['weight2'], form.cleaned_data['weight3'])

            return render(request, template, {'form': form, 'dataset': json_output})
    else:
        form = PurchaseCommodityForm()

    return render(request, template, {'form': form})




def process_data(upfile, purchase_commodity):
    csv = pd.read_csv(upfile, header = 0, names = ['Date', 'Value'], 
                        dtype= {'Date': datetime, 'Value': float}, 
                        index_col=0
    )

    for index, value in csv.iterrows():
        try:
            ts = TimeSeries.objects.create( is_purchase_commodity = True,
                                            purchase_commodity = purchase_commodity,
                                            date = index,
                                            value = value,
            )
        except Exception as e:
            print (e)
    return




def PurchaseCommodityDetailView(request, pk):
    print ("######### INSIDE PURCHASE COMMODITY DETAIL VIEW")
    template = 'CommodityTracker/commodity_benchmark.html'
    purchase_commodity = PurchaseCommodity.objects.get(pk=pk)
    json_output = _purchase_commodity_util(purchase_commodity)

    context = {'purchasecommodity': purchase_commodity  , 'dataset': json_output}
    # Render the HTML template index.html with the data in the context variable.
    return render(request, template, context)



def _purchase_commodity_util(purchase_commodity):

    print ('############# in purchase commodity util')
    purchase_commodity_name = purchase_commodity.name

    bench_name1 = purchase_commodity.benchmark1.name
    bench_name2 = purchase_commodity.benchmark2.name
    bench_name3 = purchase_commodity.benchmark3.name    

    weight1 = purchase_commodity.weight1
    weight2 = purchase_commodity.weight2
    weight3 = purchase_commodity.weight3

    # Benchmark commodity 1
    b1_queryset = TimeSeries.objects.filter(base_commodity=purchase_commodity.benchmark1)
    bench_frame1 = pd.DataFrame.from_records(b1_queryset.values('date', 'value')).set_index('date')
    bench_frame1.columns = [bench_name1]
    bench_frame1=bench_frame1.sort_index(axis=0, ascending=True)
    bench = bench_frame1
    bench['composite'] = bench[bench_name1]*(weight1/100)
    bench = bench [['composite', bench_name1]]

    if weight2 and weight2 != 0:
        # Benchmark commodity 2
        b2_queryset = TimeSeries.objects.filter(base_commodity=purchase_commodity.benchmark2)
        bench_frame2 = pd.DataFrame.from_records(b2_queryset.values('date', 'value')).set_index('date')
        bench_frame2.columns = [bench_name2]
        bench_frame2=bench_frame2.sort_index(axis=0, ascending=True)
        bench = bench.join(bench_frame2)
        bench['composite'] = bench['composite'] + bench[bench_name2]*(weight2/100)
        bench = bench [['composite', bench_name1, bench_name2]]


    if weight3 and weight3 != 0:
        # Benchmark commodity 3
        b3_queryset = TimeSeries.objects.filter(base_commodity=purchase_commodity.benchmark3)
        bench_frame3 = pd.DataFrame.from_records(b3_queryset.values('date', 'value')).set_index('date')
        bench_frame3.columns = [bench_name3]
        bench_frame3=bench_frame3.sort_index(axis=0, ascending=True)
        bench = bench.join(bench_frame3)
        bench['composite'] = bench['composite'] + bench[bench_name3]*(weight3/100)
        bench = bench [['composite', bench_name1, bench_name2, bench_name3]]


    # Extract Purchase Commodity Data
    pc_queryset = TimeSeries.objects.filter(purchase_commodity=purchase_commodity)

    purchase_frame = pd.DataFrame.from_records(pc_queryset.values('date', 'value')).set_index('date')
    purchase_frame.columns = [purchase_commodity_name]


    # reindex all to this new index
    bench = bench[purchase_frame.index[0]:]
    comb = purchase_frame.join(bench)
    comb = comb.fillna(method='ffill')
    comb = comb [['composite', purchase_commodity_name, bench_name1, bench_name2, bench_name3]]
    comb = comb.fillna(method='ffill')
    comb = comb.fillna(0)


    # convert to json and send. 
    # CONVERT TO JSON
    l = []
    for index, row in comb.iterrows():
        l.append ([index, row[purchase_commodity_name], row[bench_name1], row[bench_name2], row[bench_name3], ])
    
    lod = ([{'date': datetime.combine(date, datetime.min.time()), 
            'purchase': purch, 'benchmark_1': bench1, 'benchmark_2': bench2, 'benchmark_3': bench3} 
            for date, purch, bench1, bench2, bench3 in l])

    # Load it into gviz_api.DataTable
    desc = {'date': ('datetime', 'Date'), 
            'purchase': ('number', 'Purchase'), 
            'benchmark_1': ('number', 'Benchmark 1'),
            'benchmark_2': ('number', 'Benchmark 2'),
            'benchmark_3': ('number', 'Benchmark 3'),
            }
    data_table = gviz_api.DataTable(desc)
    data_table.LoadData(lod)

    # Create a JSon string
    json_output = data_table.ToJSon(
                            columns_order=("date", "purchase", 'benchmark_1', "benchmark_2", "benchmark_3"),
                            order_by="date"
                            )

    return json_output



































# BACKUP

def Prepare_DataFrame(purchase_commodity, weight1, weight2, weight3):
    purchase_commodity_name = purchase_commodity.name
    bench_name1 = purchase_commodity.benchmark1.name
    bench_name2 = purchase_commodity.benchmark2.name
    bench_name3 = purchase_commodity.benchmark3.name    

    # Benchmark commodity 1
    b1_queryset = TimeSeries.objects.filter(base_commodity=purchase_commodity.benchmark1)
    bench_frame1 = pd.DataFrame.from_records(b1_queryset.values('date', 'value')).set_index('date')
    bench_frame1.columns = [bench_name1]
    bench_frame1=bench_frame1.sort_index(axis=0, ascending=True)
    bench = bench_frame1
    bench['composite'] = bench[bench_name1]*(weight1/100)
    bench = bench [['composite', bench_name1]]

    if weight2 and weight2 != 0:
        # Benchmark commodity 2
        b2_queryset = TimeSeries.objects.filter(base_commodity=purchase_commodity.benchmark2)
        bench_frame2 = pd.DataFrame.from_records(b2_queryset.values('date', 'value')).set_index('date')
        bench_frame2.columns = [bench_name2]
        bench_frame2=bench_frame2.sort_index(axis=0, ascending=True)
        bench = bench.join(bench_frame2)
        bench['composite'] = bench['composite'] + bench[bench_name2]*(weight2/100)
        bench = bench [['composite', bench_name1, bench_name2]]


    if weight3 and weight3 != 0:
        # Benchmark commodity 3
        b3_queryset = TimeSeries.objects.filter(base_commodity=purchase_commodity.benchmark3)
        bench_frame3 = pd.DataFrame.from_records(b3_queryset.values('date', 'value')).set_index('date')
        bench_frame3.columns = [bench_name3]
        bench_frame3=bench_frame3.sort_index(axis=0, ascending=True)
        bench = bench.join(bench_frame3)
        bench['composite'] = bench['composite'] + bench[bench_name3]*(weight3/100)
        bench = bench [['composite', bench_name1, bench_name2, bench_name3]]


    # Extract Purchase Commodity Data
    pc_queryset = TimeSeries.objects.filter(purchase_commodity=purchase_commodity)
    print (pc_queryset)
    purchase_frame = pd.DataFrame.from_records(pc_queryset.values('date', 'value')).set_index('date')
    purchase_frame.columns = [purchase_commodity_name]
#    print (purch_frame)


#    print (purch_frame)
    # reindex all to this new index
    bench = bench[purchase_frame.index[0]:]
    comb = purchase_frame.join(bench)
    comb = comb.fillna(method='ffill')
    comb = comb [['composite', purchase_commodity_name, bench_name1, bench_name2, bench_name3]]
    comb = comb.fillna(method='ffill')
    comb = comb.fillna(0)

    print (comb)


    # convert to json and send. 
    # CONVERT TO JSON
    l = []
    for index, row in comb.iterrows():
        l.append ([index, row[purchase_commodity_name], row[bench_name1], row[bench_name2], row[bench_name3], ])
    
    lod = ([{'date': datetime.combine(date, datetime.min.time()), 
            'purchase': purch, 'benchmark_1': bench1, 'benchmark_2': bench2, 'benchmark_3': bench3} 
            for date, purch, bench1, bench2, bench3 in l])

    # Load it into gviz_api.DataTable
    desc = {'date': ('datetime', 'Date'), 
            'purchase': ('number', 'Purchase'), 
            'benchmark_1': ('number', 'Benchmark 1'),
            'benchmark_2': ('number', 'Benchmark 2'),
            'benchmark_3': ('number', 'Benchmark 3'),
            }
    data_table = gviz_api.DataTable(desc)
    data_table.LoadData(lod)

    # Create a JSon string
    json_output = data_table.ToJSon(
                            columns_order=("date", "purchase", 'benchmark_1', "benchmark_2", "benchmark_3"),
                            order_by="date"
                            )

    return json_output

