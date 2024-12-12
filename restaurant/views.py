from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.urls import reverse
from .models import  RestaurantProfile, Menu, PaymentMethod, UserProfile
from restaurant.models import PaymentMethod, RestaurantProfile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from home.models import Order, UserProfile
from django.contrib.auth.decorators import login_required

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
    username = request.user.username
    restaurant = get_object_or_404(RestaurantProfile, user_profile__user__username=username) 
    user_profile = request.user.userprofile
    if user_profile.is_restaurant():
        print(f"Restaurant ID: {restaurant.id}")  # ตรวจสอบ ID ของร้าน
        orders = Order.objects.filter(restaurant=restaurant).order_by('-order_date')
        print(f"Orders found: {orders.count()}")  # ตรวจสอบจำนวนคำสั่งซื้อ
        return render(request, 'order_list.html', {'orders': orders, 'restaurant': restaurant})     
    return render(request, "order_list.html", {'restaurant': restaurant})

def sales_report(request):      
    return render(request, "sales.html")

def edit_menu_payment(request):
    username = request.user.username
    restaurant = get_object_or_404(RestaurantProfile, user_profile__user__username=username)

    menu_items = Menu.objects.filter(restaurant_profile=restaurant)

    payment_methods = PaymentMethod.objects.filter(restaurant_profile=restaurant)  # ดึงข้อมูลการชำระเงิน
    return render(request, 'edit_menu_payment.html',{'restaurant': restaurant, 'menu_items': menu_items, 'payment_methods': payment_methods})


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
            menu_picture=menu_picture ,
            price=price
        )
        food_info.save()
        url = reverse("restaurant:edit_menu_payment")
        return redirect(f"{url}?user_type=restaurant&restaurant_name={restaurant_name}")     

    return render(request, "add_menu_res.html", {"restaurant_name": restaurant_name, 'food_categories': food_categories})



def add_payment(request):
    restaurant_profile = RestaurantProfile.objects.get(user_profile__user=request.user)
  
    error_message = None

    if request.method == 'POST':
        bank_name = request.POST.get('bank_name', '').strip()
        account_number = request.POST.get('account_number', '').strip()

        if not bank_name or not account_number:
            error_message = "กรุณากรอกชื่อธนาคารและเลขบัญชีให้ครบถ้วน"
        else:

            PaymentMethod.objects.create(
                restaurant_profile=restaurant_profile,
                bank_name=bank_name,
                account_number=account_number
            )
         
            #return redirect('restaurant:add_payment')
            return redirect('restaurant:edit_menu_payment')


    payment_methods = PaymentMethod.objects.filter(restaurant_profile=restaurant_profile)
    

    return render(request, "add_payment.html", {
        'payment_methods': payment_methods,
        'error_message': error_message
    })

def edit_only_menu(request):
    username = request.user.username
    restaurant = get_object_or_404(RestaurantProfile, user_profile__user__username=username)
    food_categories = Menu.Foodcate.choices
    is_editing = request.GET.get("edit")

    menu_id = None
    menu_item = None

    if request.method == "POST":
        menu_id = request.POST.get("menu_id")
        print("POST data:", request.POST)
        print("Menu ID received:", menu_id)
        if menu_id:
            menu_item = get_object_or_404(Menu, id=menu_id)
            if "food_name" in request.POST:
                food_name = request.POST.get("food_name").strip()
                menu_item.food_name = food_name
            elif "food_category" in request.POST:
                food_category = request.POST.get("food_category", "").strip()
                if food_category and food_category in dict(Menu.Foodcate.choices):
                    menu_item.food_category = food_category
            elif "about" in request.POST:
                about = request.POST.get("about", "").strip()
                menu_item.about = about
            elif "price" in request.POST:
                price = request.POST.get("price", "").strip()
                menu_item.price = price
            elif "restaurant_picture" in request.FILES:
                menu_picture = request.FILES["menu_picture"]
                # Save the new picture
                menu_item.menu_picture = menu_picture
                messages.success(request, "Menu picture updated successfully!")
            menu_item.save()
            return render(request, "edit_only_menu.html", {"restaurant": restaurant, "menu_item": menu_item, "menu_id": menu_id})
            
    
    elif request.method == "GET":
        menu_id = request.GET.get("menu_id")
        if menu_id:
            menu_item = get_object_or_404(Menu, id=menu_id)
    

    return render(
        request,
        "edit_only_menu.html",
        {
            "restaurant": restaurant,
            "menu_item": menu_item,
            "menu_id": menu_id,
            "food_categories": food_categories,
            "is_editing": is_editing,
        },
    )

"""   
@login_required
def restaurant_order_list(request):
    # ตรวจสอบข้อมูล restaurant ของผู้ใช้ที่ล็อกอิน
    user_profile = request.user.userprofile
    if user_profile.is_restaurant():
        restaurant = user_profile.restaurantprofile
        print(f"Restaurant ID: {restaurant.id}")  # ตรวจสอบ ID ของร้าน
        orders = Order.objects.filter(restaurant=restaurant).order_by('-order_date')
        print(f"Orders found: {orders.count()}")  # ตรวจสอบจำนวนคำสั่งซื้อ
        return render(request, 'restaurant_order_list.html', {'orders': orders})
    else:
        return redirect('home')  # หรือแสดง error message ถ้าไม่ใช่ restaurant
"""
   
@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, restaurant=request.user.userprofile.restaurantprofile)

    if request.method == 'POST':
        status = request.POST.get('status')

        if status == 'received':
            order.status = 'cooking'  # เปลี่ยนสถานะเป็น "กำลังทำอาหาร"
        elif status == 'completed':
            order.status = 'completed'  # เปลี่ยนสถานะเป็น "อาหารเสร็จแล้ว"
        
        order.save()

    return redirect('restaurant_order_list')