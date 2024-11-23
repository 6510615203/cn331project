from django.shortcuts import render
from home.models import FoodCategory 

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

def manage_restaurant(request):
    food_categories = FoodCategory.objects.all()  
    username = request.user.username  # ดึง username ของผู้ใช้

    context = {
        'food_categories': food_categories,
        'username': username,
    }
    return render(request, "manage_restaurant.html", context)