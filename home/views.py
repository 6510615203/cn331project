from django.shortcuts import render
from django.http import HttpResponseRedirect

# Create your views here.


def index(request):      
    return render(request, "index.html")

def kinkorn(request):      
    return render(request, "index.html")

def about(request):
    if request.method == "POST":
        return HttpResponseRedirect("about")      
    return render(request, "about.html")

def order(request):      
    return render(request, "index.html")

def yourorder(request):      
    return render(request, "index.html")

def login(request):      
    return render(request, "index.html")