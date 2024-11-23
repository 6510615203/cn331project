from django.shortcuts import render

# Create your views here.
def index(request):      
    return render(request, "index_restaurant.html")

def manage(request):      
    return render(request, "manage_restaurant.html")

def about(request):      
    return render(request, "about_kinkorn.html")

def order_list(request):      
    return render(request, "order_list.html")

def sales_report(request):      
    return render(request, "sales.html")