from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
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
    username = request.user.username
    restaurant = get_object_or_404(RestaurantProfile, user_profile__user__username=username)      
    return render(request, "index_restaurant.html",  {'restaurant': restaurant})

def manage(request): 
    username = request.user.username
    restaurant = get_object_or_404(RestaurantProfile, user_profile__user__username=username)
    is_editing = request.GET.get("edit")
    food_categories = RestaurantProfile.Foodcate.choices

    if request.method == "POST":
        if "restaurant_name" in request.POST:
            restaurant_name = request.POST.get("restaurant_name", "").strip()
            if restaurant_name:
                restaurant.restaurant_name = restaurant_name
        
        elif "food_category" in request.POST:
            food_category = request.POST.get("food_category", "").strip()
            if food_category and food_category in dict(RestaurantProfile.Foodcate.choices):
                restaurant.food_category = food_category

        elif "about" in request.POST:
            about = request.POST.get("about", "").strip()
            if about:
                restaurant.about = about
        
        elif "open_close_time" in request.POST:
            open_close_time = request.POST.get("open_close_time", "").strip()
            if open_close_time:
                restaurant.open_close_time = open_close_time
                
        elif "restaurant_picture" in request.FILES:
            restaurant_picture = request.FILES["restaurant_picture"]
            # Save the new picture
            restaurant.restaurant_picture = restaurant_picture
            messages.success(request, "Profile picture updated successfully!")

        restaurant.save()  # Save all updates to the database
        return redirect("restaurant:manage")  # Redirect to refresh and show updates

    
    return render(request, "manage_restaurant.html", {'restaurant': restaurant, "is_editing": is_editing,'food_categories': food_categories})

def about(request):      
    return render(request, "about_kinkorn.html")

def order_list(request):      
    return render(request, "order_list.html")

def sales_report(request):      
    return render(request, "sales.html")

def edit_menu_payment(request):
    username = request.user.username
    restaurant = get_object_or_404(RestaurantProfile, user_profile__user__username=username)

    menu_items = Menu.objects.filter(restaurant_profile=restaurant)

    return render(request, 'edit_menu_payment.html',{'restaurant': restaurant, 'menu_items': menu_items})


def add_menu_res(request):
    username = request.user.username
    restaurant = get_object_or_404(RestaurantProfile, user_profile__user__username=username)
    restaurant_name = restaurant.restaurant_name
    food_categories = RestaurantProfile.Foodcate.choices
    if request.method == "POST":
        food_name = request.POST.get("food_name")
        food_category = request.POST.get("food_category")
        about = request.POST.get("about")
        price = request.POST.get("price")
        user_type = request.POST.get("user_type")
        
        # รับไฟล์รูปภาพจากฟอร์ม
        if 'menu_picture' in request.FILES:
            menu_picture = request.FILES['menu_picture']
            fs = FileSystemStorage()
            filename = fs.save(menu_picture.name, menu_picture) 
            menu_picture_url = fs.url(filename)  
        else:
            menu_picture_url = None

        restaurant_profile = get_object_or_404(RestaurantProfile, restaurant_name=restaurant_name)

        food_info = Menu.objects.create(
            restaurant_profile=restaurant_profile,
            food_name=food_name, 
            food_category=food_category, 
            about=about,
            menu_picture=menu_picture_url ,
            price=price
        )
        food_info.save()
        url = reverse("restaurant:edit_menu_payment")
        return redirect(f"{url}?user_type=restaurant&restaurant_name={restaurant_name}")     

    return render(request, "add_menu_res.html", {"restaurant_name": restaurant_name, 'food_categories': food_categories})

def add_payment(request):
    return render(request, "add_payment.html")