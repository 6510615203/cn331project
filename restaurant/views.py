from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.urls import reverse
from home.models import UserProfile, RestaurantProfile, Menu,FoodCategory
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage

# Create your views here.
def index(request):
    username = request.user.username
    restaurant = get_object_or_404(RestaurantProfile, user_profile__user__username=username)      
    return render(request, "index_restaurant.html",  {'restaurant': restaurant})


def manage(request):
    username = request.user.username
    restaurant = get_object_or_404(RestaurantProfile, user_profile__user__username=username)
    is_editing = request.GET.get("edit")  # ตรวจสอบค่าจาก query parameter
    food_categories = FoodCategory.objects.all()

    if request.method == "POST":
        if is_editing == "restaurant_name":
            restaurant_name = request.POST.get("restaurant_name", "").strip()
            if restaurant_name:
                restaurant.restaurant_name = restaurant_name
        elif is_editing == "food_category":
            food_category_id = request.POST.get("food_category")  
            food_category = get_object_or_404(FoodCategory, id=food_category_id)
            restaurant.food_category = food_category
        elif is_editing == "about":
            about = request.POST.get("about", "").strip()
            if about:
                restaurant.about = about
        elif is_editing == "open_close_time":
            open_close_time = request.POST.get("open_close_time", "").strip()
            if open_close_time:
                restaurant.open_close_time = open_close_time

        restaurant.save()
        return redirect("restaurant:manage")  

    return render(request, "manage_restaurant.html", {
        "restaurant": restaurant,
        "is_editing": is_editing,
        "food_categories": food_categories,  
    })

def about(request):      
    return render(request, "about_kinkorn.html")

def order_list(request):      
    return render(request, "order_list.html")

def sales_report(request):      
    return render(request, "sales.html")