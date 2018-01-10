from django.conf.urls import include, url
from customeranalytics import views


urlpatterns = [
    url(r'^$', views.CustomerAnalyticsHome, name='customer-analytics-home'),
]

# Company Urls
urlpatterns += [
    url(r'^companies/$', views.CompanyListView.as_view(), name='companies'),
    url(r'company/(?P<pk>\d+)$', views.CompanyDetailView.as_view(), name='company-detail'),
]


# Branch Urls
urlpatterns += [
    url(r'branches/$', views.BranchListView.as_view(), name='branches'),
    url(r'branch/(?P<pk>\d+)$', views.BranchDetailView.as_view(), name='branch-detail'),
]


# Occassion Urls
urlpatterns += [
    url(r'occassions/$', views.OccassionListView.as_view(), name='occassions'),
    url(r'occassion/(?P<pk>\d+)$', views.OccassionDetailView.as_view(), name='occassion-detail'),
]

# Customer Urls
urlpatterns += [
    url(r'customers/$', views.customer_list, name='customers'),
    url(r'customer/(?P<pk>\d+)$', views.CustomerDetailView.as_view(), name='customer-detail'),
    url(r'customer/update/$', views.update_customers, name='customer-update'),
]

# Order Urls
urlpatterns += [
    url(r'^orders/$', views.OrderListView.as_view(), name='orders'),
    url(r'order/(?P<pk>\d+)$', views.OrderDetailView.as_view(), name='order-detail'),
]


# Form Handling
urlpatterns += [   
    url(r'^data/$', views.data_upload, name='data-upload'),
]

urlpatterns += [  
    url(r'^profile/create/$', views.update_profile, name='profile_create'),
]
