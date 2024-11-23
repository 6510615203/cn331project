from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.urls import reverse
from .models import UserProfile, RestaurantProfile, Menu
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage

# Create your views here.
def index(request):      
    return render(request, "index_restaurant.html")

def manage(request): 
    username = request.user.username
    restaurant = get_object_or_404(RestaurantProfile, user_profile__user__username=username)
    is_editing = request.GET.get("edit")

    if request.method == "POST":
        if "restaurant_name" in request.POST:
            restaurant_name = request.POST.get("restaurant_name", "").strip()
            if restaurant_name:
                restaurant.restaurant_name = restaurant_name
        
        elif "food_category" in request.POST:
            food_category = request.POST.get("food_category", "").strip()
            if food_category:
                restaurant.food_category = food_category

        elif "about" in request.POST:
            about = request.POST.get("about", "").strip()
            if about:
                restaurant.about = about
        
        elif "open_close_time" in request.POST:
            open_close_time = request.POST.get("open_close_time", "").strip()
            if open_close_time:
                restaurant.open_close_time = open_close_time
        

        restaurant.save()
        return redirect("restaurant:manage")

    
    return render(request, "manage_restaurant.html", {'restaurant': restaurant, "is_editing": is_editing,})

def about(request):      
    return render(request, "about_kinkorn.html")

def order_list(request):      
    return render(request, "order_list.html")

def sales_report(request):      
    return render(request, "sales.html")