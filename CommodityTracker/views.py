from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.generic.edit import View, CreateView, UpdateView, DeleteView
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.urls import reverse_lazy
import datetime
from datetime import timedelta
from datetime import datetime
from datetime import date

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
import numpy as np
import gviz_api

# Create your views here.

class CommodityHome(generic.ListView):
    model = Category
    template_name = 'CommodityTracker/purchasing_home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['purchasecommodity_list'] = PurchaseCommodity.objects.all()
        return context

    def get_queryset(self):
        return Category.objects.all().order_by('name')


class CategoryListView(generic.ListView):
    model = Category
    template_name = 'CommodityTracker/category_list.html'

    def get_queryset(self):
        return Category.objects.all().order_by('name')

class CategoryDetailView(generic.DetailView):
    model = Category

class BaseCommodityListView(generic.ListView):
    model = BaseCommodity
    template_name = 'CommodityTracker/basecommodity_list.html'

    def get_queryset(self):
        return BaseCommodity.objects.all().order_by('name')



class BaseCommodityDetailView(generic.DetailView):
    template = 'CommodityTracker/basecommodity_detail.html'
    model = BaseCommodity

    def get_context_data(self, **kwargs):
        context = super(BaseCommodityDetailView, self).get_context_data(**kwargs)
        base_commodity = self.object

        # if required, update the dataset
        if base_commodity.needs_update():
            status = base_commodity.update_data()
    #        print ("Update status: " + status)

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


        context ['dataset'] = json_output
        return context


def _BaseCommodityDetailView(request, pk):
    template = 'CommodityTracker/basecommodity_detail.html'
    base_commodity = BaseCommodity.objects.get(pk=pk)
#    print (base_commodity)

    # if required, update the dataset
    if base_commodity.needs_update():
        status = base_commodity.update_data()
#        print ("Update status: " + status)

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



def PurchasingIndexView(request):
    return render( request, 'CommodityTracker/purchasing_home.html',)

class PurchaseCommodityListView(generic.ListView):
    model = PurchaseCommodity
    template_name = 'CommodityTracker/purchasecommodity_list.html'

    def get_queryset(self):
        return PurchaseCommodity.objects.all().order_by('name')

class PurchaseCommodityDetailView(generic.DetailView):
    template = 'CommodityTracker/purchasecommodity_detail.html'
    model = PurchaseCommodity

    def get_context_data(self, **kwargs):
        context = super(PurchaseCommodityDetailView, self).get_context_data(**kwargs)
        purchase_commodity = self.object
        json_output = _purchase_commodity_util(purchase_commodity)
        context ['dataset'] = json_output
        return context

















class PurchaseCommodityCreate(CreateView):
    model = PurchaseCommodity
    template_name = 'CommodityTracker/generic_form.html'
    form_class = PurchaseCommodityForm


    def form_valid(self, form):
        print ('posted something. let us add logic to save file')
        self.object = form.save(commit=False)
        self.object.last_updated = date.today()

        self.object.name = form.cleaned_data['name']
        self.object.description = form.cleaned_data['description'] 
        self.object.company_name = form.cleaned_data['company_name']
        self.object.last_updated = date.today()
        self.object.weight1 = form.cleaned_data['weight1']
        self.object.weight2 = form.cleaned_data['weight2']
        self.object.weight3 = form.cleaned_data['weight3']
        self.object.benchmark1 = form.cleaned_data['benchmark1']
        self.object.benchmark2 = form.cleaned_data['benchmark2']
        self.object.benchmark3 = form.cleaned_data['benchmark3']

        self.object.save()
        super().form_valid(form)

        process_data(self.request.FILES['commodity_purchase_data'], self.object)

        json_output = _purchase_commodity_util(self.object)
        context = {'purchasecommodity': self.object, 'dataset': json_output}

        return render(self.request, "CommodityTracker/purchasecommodity_detail.html", context)




# YES
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

            json_output = _purchase_commodity_util(purchase_commodity)
            context = {'purchasecommodity': purchase_commodity, 'dataset': json_output}

            return render(request, "CommodityTracker/purchasecommodity_detail.html", context)
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


def _purchase_commodity_util(purchase_commodity):

    purchase_commodity_name = purchase_commodity.name

    bench_name1 = purchase_commodity.benchmark1.name
    bench_name2 = purchase_commodity.benchmark2.name
    bench_name3 = purchase_commodity.benchmark3.name    

    weight1 = purchase_commodity.weight1/100
    weight2 = purchase_commodity.weight2/100
    weight3 = purchase_commodity.weight3/100

    # Benchmark commodity 1
    b1_queryset = TimeSeries.objects.filter(base_commodity=purchase_commodity.benchmark1)
    bench_frame1 = pd.DataFrame.from_records(b1_queryset.values('date', 'value')).set_index('date')
    bench_frame1.columns = [bench_name1]
    bench = bench_frame1
    bench['composite'] = bench[bench_name1]*(weight1)
    bench = bench [['composite', bench_name1]]


    if weight2 != 0:
        # Benchmark commodity 2
        b2_queryset = TimeSeries.objects.filter(base_commodity=purchase_commodity.benchmark2)
        bench_frame2 = pd.DataFrame.from_records(b2_queryset.values('date', 'value')).set_index('date')
        bench_frame2.columns = [bench_name2]
        bench = bench.join(bench_frame2)
    else: 
        bench_name2 = 'Benchmark2'
        bench [bench_name2] = 0


    if weight3 != 0:
        # Benchmark commodity 3
        b3_queryset = TimeSeries.objects.filter(base_commodity=purchase_commodity.benchmark3)
        bench_frame3 = pd.DataFrame.from_records(b3_queryset.values('date', 'value')).set_index('date')
        bench_frame3.columns = [bench_name3]
        bench = bench.join(bench_frame3)
    else:
        bench_name3 = 'Benchmark3'
        bench [bench_name3] = 0

    # Create Composite
    bench['composite'] = bench[bench_name1]*(weight1) + bench[bench_name2]*(weight2) + bench[bench_name3]*(weight3)

    # Extract Purchase Commodity Data
    pc_queryset = TimeSeries.objects.filter(purchase_commodity=purchase_commodity)
    purchase_frame = pd.DataFrame.from_records(pc_queryset.values('date', 'value')).set_index('date')
    purchase_frame.columns = [purchase_commodity_name]

    # CREATE INDEX
    periods = (datetime.utcnow() - purchase_frame.index[0].tz_convert(None)).days
    index_dates = pd.date_range(purchase_frame.index[0], periods=periods, freq='D')

    # reindex all to this new index
    comb = pd.DataFrame(purchase_frame, index=index_dates).join(bench).fillna(method='ffill').fillna(0)
    comb = comb [['composite', purchase_commodity_name, bench_name1, bench_name2, bench_name3]]

    # convert to json and send. 
    # CONVERT TO JSON
    l = []
    for index, row in comb.iterrows():
        l.append ([index, 
                    row[purchase_commodity_name], 
                    row['composite'], 
                    row[bench_name1], 
                    row[bench_name2], 
                    row[bench_name3],
                  ])

    lod = ([{'date': datetime.combine(date, datetime.min.time()), 
            'purchase': purch, 
            'composite': comp , 
            'benchmark_1': bench1, 
            'benchmark_2': bench2, 
            'benchmark_3': bench3} 
            for date, purch, comp, bench1, bench2, bench3 in l])

    # Load it into gviz_api.DataTable
    desc = {'date': ('datetime', 'Date'), 
            'purchase': ('number', 'Purchase'), 
            'composite': ('number', 'Composite'),
            'benchmark_1': ('number', bench_name1),
            'benchmark_2': ('number', bench_name2),
            'benchmark_3': ('number', bench_name3),
            }
    data_table = gviz_api.DataTable(desc)
    data_table.LoadData(lod)

    # Create a JSon string
    json_output = data_table.ToJSon(
                            columns_order=("date", "purchase", 'composite', 'benchmark_1', "benchmark_2", "benchmark_3"),
                            order_by="date"
                            )

    return json_output







"""
Admin accessible init functions

"""
# YES
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
#    print ('udpate completed')

    return render( request, 'CommodityTracker/test_page.html',)


