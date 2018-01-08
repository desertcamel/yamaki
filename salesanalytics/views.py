from django.shortcuts import render

# Create your views here.

def SalesAnalyticsHome(request):
    return render( request, 'salesanalytics/home.html',)

def VizHome(request):

    context = {
        'value' : 'http%3A%2F%2Fdashboards.biznessanalytics.com%2F',
        'width' : '100%',
        'height' : '100%', 
        'host_url' : 'http%3A%2F%2Fdashboards.biznessanalytics.com%2F',
        'embed_code_version' : '2',
        'site_root' : '&#47;t&#47;Misterbaker',
        'name' : 'SalesDashboards_Beta&#47;Home',
        'tabs' : 'yes',
        'toolbar' :'yes',
        'showAppBanner' :'false',
        'showShareOptions' : 'true',
    }    

    return render( request, 'viz.html', context)
