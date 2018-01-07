from django.shortcuts import render

# Create your views here.

def SalesAnalyticsHome(request):
    return render( request, 'salesanalytics/home.html',)
