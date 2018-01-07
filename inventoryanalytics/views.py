from django.shortcuts import render

# Create your views here.

def InventoryAnalyticsHome(request):
    return render( request, 'inventoryanalytics/home.html',)
