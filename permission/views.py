from django.shortcuts import render, HttpResponse
import datetime
# Create your views here.

def testRoutes(request):

    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)