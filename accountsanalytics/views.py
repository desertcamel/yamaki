from django.shortcuts import render

# Create your views here.

def AccountsAnalyticsHome(request):
    return render( request, 'accountsanalytics/home.html',)
