from django.conf.urls import include, url

from . import views


urlpatterns = [
    url(r'^$', views.CommodityListView.as_view(), name='commodities-list'),
    url(r'purchasing/$', views.PurchasingIndexView, name='purchasing-index-home'),
]

# List Urls
urlpatterns += [
    # Detail
    url(r'category/(?P<pk>\d+)$', views.CategoryDetailView.as_view(), name='category-detail'),
    url(r'commodity/(?P<pk>\d+)$', views.CommodityDetailView, name='commodity-detail'),
    url(r'commodity/(?P<base_pk>\d+)/benchmark/(?P<bench_pk>\d+)$', views.CommodityBenchmarkView, name='benchmark-commodity'),
]

# List Urls
urlpatterns += [
    # Create
    url(r'category/add/$', views.CategoryCreateView.as_view(), name='new-category'),
    url(r'commodity/add/$', views.CategoryCreateView.as_view(), name='new-commodity'),
]

urlpatterns += [
    url(r'^signup/$', views.SignUpView.as_view(), name='signup'),
    url(r'^signup/ajax/validate_username/$', views.validate_username, name='validate-username'),
]


