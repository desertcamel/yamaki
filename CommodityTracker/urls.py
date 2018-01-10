from django.conf.urls import include, url

from . import views

# Home Page
urlpatterns = [
    url(r'^$', views.CommodityHome.as_view(), name='commodity-analytics-home'),
]

# Base Commodities
urlpatterns += [
    url(r'categories/$', views.CategoryListView.as_view(), name='category-list'),
    url(r'category/(?P<pk>\d+)$', views.CategoryDetailView.as_view(), name='category-detail'),
    url(r'base_commodities/$', views.BaseCommodityListView.as_view(), name='base-commodity-list'),
    url(r'base_commodity/(?P<pk>\d+)$', views.BaseCommodityDetailView.as_view(), name='base-commodity-detail'),
]

# Purchase Commodities
urlpatterns += [
    url(r'purchase_commodities/$', views.PurchaseCommodityListView.as_view(), name='purchase-commodity-list'),
    url(r'purchase_commodity/(?P<pk>\d+)$', views.PurchaseCommodityDetailView.as_view(), name='purchase-commodity-detail'),
    url(r'^purchase_commodity_create/$', views.PurchaseCommodityCreate.as_view(), name='purchase-commodity-add'),
]

# Admin Functions
urlpatterns += [
    url(r'^init/$', views.app_init, name='app-init'),
]



