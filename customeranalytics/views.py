from django.shortcuts import render


from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required

from .models import Company, Branch, Customer, Order, Occassion, Document
from django.urls import reverse, reverse_lazy

from .forms import DocumentForm
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.storage import FileSystemStorage

import pandas as pd
import csv
import json


# Create your views here.

def CustomerAnalyticsHome(request):
    """
    View function for home page of site.
    """
    # Generate counts of some of the main objects
    num_branch=Branch.objects.all().count()
    num_customers=Customer.objects.all().count()
    num_occassions=Occassion.objects.all().count()
    num_orders=Order.objects.all().count()


    # SESSION TRACKER
    # Number of visits to this view, as counted in the session variable.
    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1


    # Render the HTML template index.html with the data in the context variable.
    return render(
        request,
        'celebration/index.html',
        context={'num_branch':num_branch,'num_customers':num_customers,'num_occassions':num_occassions, 
        'num_orders':num_orders, 'num_visits':num_visits}, # num_visits appended
    )




def index(request):
    """
    View function for home page of site.
    """
    # Generate counts of some of the main objects
    num_branch=Branch.objects.all().count()
    num_customers=Customer.objects.all().count()
    num_occassions=Occassion.objects.all().count()
    num_orders=Order.objects.all().count()


    # SESSION TRACKER
    # Number of visits to this view, as counted in the session variable.
    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1


    # Render the HTML template index.html with the data in the context variable.
    return render(
        request,
        'celebration/index.html',
        context={'num_branch':num_branch,'num_customers':num_customers,'num_occassions':num_occassions, 
        'num_orders':num_orders, 'num_visits':num_visits}, # num_visits appended
    )



# Company
class CompanyListView(generic.ListView):
    model = Company
    paginate_by = 5

    def get_queryset(self):
        return Company.objects.all().order_by('company_name')

class CompanyDetailView(generic.DetailView):
    model = Company

class CompanyCreate(CreateView):
    model = Company
    fields = '__all__'

class CompanyUpdate(UpdateView):
    model = Company
    fields = '__all__'

class CompanyDelete(DeleteView):
    model = Company
    success_url = reverse_lazy('index')



# Branch
from django.db.models import Count

def  branch_list(request):
    template = 'celebration/branch_list.html'
    branch_list = Branch.objects.order_by('branch_name')
    
    sample_data = [['Branch', 'Count']]
    branches = Branch.objects.values('branch_name', order_count=Count('order')).order_by('order_count')

    for b in branches:
        sample_data3 = [[b['branch_name'], b['order_count']]]
        sample_data += sample_data3

    # create context to pass 
    context = {
        'branch_list': branch_list,
        'data_table': json.dumps(sample_data),
    }
    # Render the HTML template index.html with the data in the context variable.
    return render(request, template, context)










class BranchDetailView(generic.DetailView):
    model = Branch


class BranchCreate(CreateView):
    model = Branch
    fields = '__all__'

class BranchUpdate(UpdateView):
    model = Branch
    fields = '__all__'

class BranchDelete(DeleteView):
    model = Branch
    success_url = reverse_lazy('index')


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

# Customer List View
def  customer_list(request):
    template = 'celebration/customer_list.html'
    customer_list = Customer.objects.order_by('customer_name')

    paginator = Paginator(customer_list, 25) # Show # contacts per page
    page = request.GET.get('page')
    customer_list = paginator.get_page(page)


    sample_data = [['Customer', 'Count']]
    customers = Customer.objects.values('customer_name', order_count=Count('order')).order_by('order_count')

    for b in customers:
        sample_data3 = [[b['customer_name'], b['order_count']]]
        sample_data += sample_data3

    # create context to pass 
    context = {
        'customer_list': customer_list,
        'data_table': json.dumps(sample_data),
    }
    # Render the HTML template index.html with the data in the context variable.
    return render(request, template, context)



class CustomerDetailView(generic.DetailView):
    model = Customer


# Update Customers
from django.forms import modelform_factory, modelformset_factory, inlineformset_factory
from .forms import OrderForm
from django.shortcuts import render
def update_customers(request):
    CustomerFormset = modelformset_factory(Customer, fields='__all__')
    formset = CustomerFormset(queryset = Customer.objects.filter(customer_name__startswith="a"))

    order_form = OrderForm()

    if request.method == 'POST':
        formset = CustomerFormset(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()
    elif request.method == 'GET':
        # FINISH ALL SEARCH QUERY COMBINATION
        order_form = OrderForm(request.GET)
        if order_form.is_valid:
            if len (request.GET) > 0: 
                q_branch = Branch.objects.get(id=request.GET['Branch'])
                q_company = Company.objects.get(id=request.GET['Company'])
                q_occassion = Occassion.objects.get(id=request.GET['Occassion'])
                q_customer = Customer.objects.filter(order__Branch=q_branch, order__Company=q_company, order__Occassion=q_occassion).order_by('customer_name')[:50]
            else:
                q_customer = Customer.objects.filter(order__Branch__id = 1).order_by('customer_name')[:50]

            formset = CustomerFormset(queryset = q_customer)
    else:
        qset  = Customer.objects.filter(customer_name__startswith="a").order_by('customer_name')[:50]
        formset = CustomerFormset(queryset = qset)

    return render(request, 'celebration/customer_update.html', {'formset': formset, 'order_form': order_form})        


# Occassion
class OccassionListView(generic.ListView):
    model = Occassion
    template_name = 'celebration/order_list.html'
    paginate_by = 200

    def get_queryset(self):
        return Occassion.objects.all().order_by('occassion_name')

class OccassionDetailView(generic.DetailView):
    model = Occassion





# Order
class OrderListView(generic.ListView):
    model = Order
    template_name = 'celebration/order_list.html'
    paginate_by = 200

    def get_queryset(self):
        return Order.objects.all().order_by('-Order_Date')

class OrderDetailView(generic.DetailView):
    model = Order


# FORMS HANDLING
def data_upload(request):
 
    # If this is a POST request then process the Form data
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)

        if form.is_valid():
            file = Document()
            file.name = form.cleaned_data['name']
            file.file = form.cleaned_data['file']
#            file.save()
            process_data(request.FILES['file'])
#            handle_file(request.FILES['file'])
            return HttpResponseRedirect(reverse('orders'))

    # If this is a GET (or any other method) create the default form.
    else:
        form = DocumentForm()

    return render(request, 'celebration/file_upload.html', {'form': form})



def process_data(upfile):

    import pandas as pd

    xls = pd.read_excel(upfile)

    company_name = 'Misterbaker LLC'

    branch_alias_dict = {
        'KMA': 'Karama'
    }


    occassion_alias_dict = {
        'H/B': 'Birthday', 
        'HB': 'Birthday', 
        'hb': 'Birthday', 
        'ANN': 'Anniversary', 
        'ANNIV': 'Anniversary', 
        'ANNIV.': 'Anniversary',
        'ANNNI': 'Anniversary',
        'ANNIV.': 'Anniversary',
        'ANNIVERSARY': 'Anniversary',
        'B TRANS': 'Branch Transfer',
        'B.TRANS.': 'Branch Transfer',
        'B TRANSFER': 'Branch Transfer',
        'B. TRANSFER': 'Branch Transfer',
        'B.T': 'Branch Transfer',
        'B.TRANSFER': 'Branch Transfer',
        'B/TRANS': 'Branch Transfer',
        'BT': 'Branch Transfer',
    }

    col_name_map = {
        'Branch': 'Branch',
        'Order Date': 'Order_Date',
        'Delivery Date': 'Delivery_Date',
        'Customer Name': 'Customer_Name',
        'Order #': 'Order_No', 
        'Contact #': 'Contact_No', 
        'Total Amount': 'Total_Amount', 
        'Remarks': 'Occassion',
    }

    xls=xls.rename(columns=col_name_map, index=str)

    xls = xls[['Branch', 'Order_Date', 'Delivery_Date', 'Customer_Name', 'Order_No', 'Contact_No', 'Total_Amount', 'Occassion']]

    # Clean Data
    xls.dropna(subset=['Contact_No'], inplace=True)
    xls['Occassion'] = xls['Occassion'].fillna('Not Mentioned')
    xls['Total_Amount'] = xls['Total_Amount'].fillna(0)
    xls['Order_Date'] = xls['Order_Date'].fillna(method='ffill')
    xls['Delivery_Date'] = xls['Delivery_Date'].fillna(method='ffill')
    xls['Branch'] = xls['Branch'].fillna(method='ffill')
    

    xls[['Order_Date']] = xls[['Order_Date']].apply(pd.to_datetime, errors='coerce')
    xls[['Order_No', 'Contact_No', 'Total_Amount',]] = xls[['Order_No', 'Contact_No', 'Total_Amount',]].apply(pd.to_numeric, errors='coerce')

    xls['Contact_No'] = xls['Contact_No'].fillna(0.0).astype(int)

    xls['Branch'] = xls['Branch'].replace(branch_alias_dict)
    xls['Occassion'] = xls['Occassion'].replace(occassion_alias_dict)


    dict_list = xls.to_dict('records')

    for i in dict_list:
        print ('$$%$%$%%&####### PARSING DICT ##################')
        try:
            # Create order 
            new_order, created = Order.objects.get_or_create(Order_No__exact=i['Order_No'])
            if created:
                print ('############# NEW ORDER ENTRY START ##################')
                new_order.Company, c0 = Company.objects.get_or_create(
                    company_name = company_name,
                )
                new_order.Order_No = i['Order_No']
                new_order.Order_Date = i['Order_Date']
                new_order.Total_Amount = i['Total_Amount']
                new_order.Customer, c1 = Customer.objects.get_or_create(
                                    phone_number = i['Contact_No'],
                                    customer_name = i['Customer_Name']
                                    )
                new_order.Occassion, c2 = Occassion.objects.get_or_create(occassion_name = i['Occassion'])
                new_order.Branch, c3 = Branch.objects.get_or_create(branch_name = i['Branch'], company_name = new_order.Company )

                new_order.save()
                print ('converted'+str(i))
            else:
                print ('entry already exists')
        except Exception as e:
            print ('error')
            print (e)



# USER PROFILE
from .models import Profile

class ProfileCreate(CreateView):
    model = Profile
    fields = '__all__'



from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from .forms import UserForm, ProfileForm


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, ('Your profile was successfully updated!'))
            return redirect('index')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'celebration/profile_form.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })