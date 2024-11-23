from django.shortcuts import render

# Create your views here.
def index(request):      
    user_type = request.GET.get('user_type', 'default_value') 
    username = request.GET.get('username', 'default_value')
    restaurant_name= request.GET.get('restaurant_name', 'default_value')

    context = {
        'user_type': user_type,
        'username': username,
        'restaurant_name': restaurant_name,
    }
    return render(request, "index_restaurant.html", context)

def manage(request):      
    return render(request, "manage_restaurant.html")

def about(request):      
    return render(request, "about_kinkorn.html")

def order_list(request):      
    return render(request, "order_list.html")

def sales_report(request):      
    return render(request, "sales.html")