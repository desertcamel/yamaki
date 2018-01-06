from django.conf.urls import include, url

from . import views


urlpatterns = [
    url(r'^$', views.CommodityListView.as_view(), name='commodities-list'),
]

urlpatterns += [
    url(r'^init/$', views.app_init, name='app-init'),
    url(r'purchasing/$', views.PurchasingIndexView, name='purchasing-index-home'),
    url(r'purchasingform/$', views.purchase_commodity_form, name='purchasing-form'),
]
urlpatterns += [
    url(r'commodity/(?P<base_pk>\d+)/benchmark/(?P<bench_pk>\d+)$', views.CommodityBenchmarkView, name='benchmark-commodity'),
]

# List Urls
urlpatterns += [
    # Detail
    url(r'categories/$', views.CategoryListView.as_view(), name='category-list'),
    url(r'base_commodities/$', views.BaseCommodityListView.as_view(), name='base-commodity-list'),
    url(r'purchase_commodities/$', views.PurchaseCommodityListView.as_view(), name='purchase-commodity-list'),
    url(r'time_series/$', views.TimeSeriesListView.as_view(), name='time-series-list'),
]

# Detail Urls
urlpatterns += [
    # Detail
    url(r'category/(?P<pk>\d+)$', views.CategoryDetailView.as_view(), name='category-detail'),
    url(r'base_commodity/(?P<pk>\d+)$', views.BaseCommodityDetailView, name='base-commodity-detail'),
    url(r'purchase_commodity/(?P<pk>\d+)$', views.PurchaseCommodityDetailView, name='purchase-commodity-detail'),
    url(r'timeseries_detail/(?P<pk>\d+)$', views.TimeSeriesDetailView.as_view(), name='timeseries-detail'),
]


# List Urls
urlpatterns += [
    # Create
    url(r'category/add/$', views.CategoryCreateView.as_view(), name='new-category'),
    url(r'commodity/add/$', views.CategoryCreateView.as_view(), name='new-commodity'),
]



