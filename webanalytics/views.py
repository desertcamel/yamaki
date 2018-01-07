from django.shortcuts import render

# Create your views here.

def WebAnalyticsHome(request):
    return render( request, 'webanalytics/home.html',)
