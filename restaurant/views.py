from django.utils import timezone
import decimal
from email.utils import parsedate
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
from django.db.models import Sum
from django.db.models import Count
from django.db.models import Q
from datetime import datetime
from django.test import TestCase, Client
# Create your views here.
def index(request):
    username = request.user.username
    restaurant = get_object_or_404(RestaurantProfile, user_profile__user__username=username)
    order_counts = (
        Order.objects.filter(restaurant=restaurant)
        .values('status')
        .annotate(count=Count('id'))
    )

    waiting_payment_counts = Order.objects.filter(
        Q(restaurant=restaurant) & (
            Q(status='waiting_for_payment') | 
            Q(status='waiting_for_approve') | 
            Q(status='paid')
        )
    ).exclude(id__in=Order.objects.filter(status='cooking').values('id')).count()
    paid_orders_not_started = Order.objects.filter(Q(restaurant=restaurant) & Q(status='paid')).count()
    cooking_counts = Order.objects.filter(Q(restaurant=restaurant) & (Q(status='cooking') )).count()
    completed_counts = Order.objects.filter(restaurant=restaurant, status='completed').count()

    context = {
        'restaurant': restaurant,
        'order_counts': order_counts,
        'waiting_payment_counts': waiting_payment_counts,
        'cooking_counts': cooking_counts,
        'completed_counts': completed_counts

    }

    return render(request, "index_restaurant.html",  context)

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

@login_required
def order_list(request):
    username = request.user.username
    restaurant = get_object_or_404(RestaurantProfile, user_profile__user__username=username)

    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        action = request.POST.get('action')

     
        order = Order.objects.get(id=order_id, restaurant=restaurant)

        if action == 'confirm_payment':
            # ยืนยันการชำระเงิน
            order.status = 'paid'
            order.save()
            messages.success(request, f"Order {order.id}: Payment confirmed.")
            
        elif action == 'mark_in_progress':
            # เริ่มทำอาหาร
            order.status = 'cooking'
            messages.success(request, f"Order {order.id}: Order is now in progress.")
        elif action == 'mark_completed':
            # ออร์เดอร์เสร็จสมบูรณ์
            order.status = 'completed'
            messages.success(request, f"Order {order.id}: Order completed.")
        order.save()

        
        return redirect('restaurant:order_list')  # เปลี่ยนเส้นทางไปยังหน้า order_list หลังจากอัปเดต

    # ดึงคำสั่งซื้อทั้งหมดของร้านอาหาร
    orders = Order.objects.filter(restaurant=restaurant).order_by('-order_date')

    return render(request, 'order_list.html', {'orders': orders, 'restaurant': restaurant})


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
        
        menu_picture = None 
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

def edit_only_menu(request):
    username = request.user.username
    restaurant = get_object_or_404(RestaurantProfile, user_profile__user__username=username)
    food_categories = Menu.Foodcate.choices
    is_editing = request.GET.get("edit")

    menu_id = None
    menu_item = None

    if request.method == "POST":
        menu_id = request.POST.get("menu_id")
        if not menu_id:
            return HttpResponse(status=404)
        if menu_id:
            menu_item = get_object_or_404(Menu, id=menu_id)
            if request.POST.get('delete_menu') == 'true':
                menu_item.delete()
                messages.success(request, f"Menu '{menu_item.food_name}' deleted successfully.")
                return redirect('restaurant:edit_menu_payment')
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
            elif "menu_picture" in request.FILES:
                menu_picture = request.FILES["menu_picture"]
                if menu_picture:
                    menu_item.menu_picture = menu_picture
                    menu_item.save()
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

from django.utils import timezone
@login_required
def order_confirmation(request, order_id):
    user_profile = request.user.userprofile
    restaurant_profile = user_profile.restaurantprofile_set.first()

    order = get_object_or_404(Order, id=order_id, restaurant=restaurant_profile)

    if request.method == 'POST':
        status = request.POST.get('status')

        if status == 'paid':
            order.status = 'paid'
        elif status == 'cooking':
            order.status = 'cooking'
        elif status == 'completed':
            order.status = 'completed'
            order.completed_at = timezone.now()

        order.save()

    return redirect('restaurant:order_list')



from django.utils.dateparse import parse_date
from django.db.models import Sum

@login_required
def sales_report(request):
    username = request.user.username
    restaurant = get_object_or_404(RestaurantProfile, user_profile__user__username=username)

    # รับค่าจาก query parameters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # ดึงคำสั่งซื้อที่สถานะเป็น completed
    orders = Order.objects.filter(restaurant=restaurant, status='completed')

    # ถ้ามีการกรอง start_date
    if start_date:
        start_date = parse_date(start_date)  # แปลง start_date เป็นวันที่
        orders = orders.filter(order_date__date__gte=start_date)  # ใช้ฟิลด์ order_date ในการกรอง

    # ถ้ามีการกรอง end_date
    if end_date:
        end_date = parse_date(end_date)  # แปลง end_date เป็นวันที่
        orders = orders.filter(order_date__date__lte=end_date)

    # คำนวณยอดขายรวม
    total_sales = orders.aggregate(Sum('total_price'))['total_price__sum'] or 0

    return render(request, 'sales_report.html', {
        'restaurant': restaurant,
        'orders': orders,
        'total_sales': total_sales,
        'start_date': start_date,
        'end_date': end_date,
    })


def add_payment(request):

    restaurant_profile = RestaurantProfile.objects.get(user_profile__user=request.user)
    error_message = None

    if request.method == 'POST':
        bank_name = request.POST.get('bank_name', '').strip()
        account_number = request.POST.get('account_number', '').strip()

        # ตรวจสอบว่าชื่อธนาคารหรือเลขบัญชีว่างเปล่า
        if not bank_name or not account_number:
            error_message = "กรุณากรอกชื่อธนาคารและเลขบัญชีให้ครบถ้วน"
        # ตรวจสอบว่าเลขบัญชีเป็นตัวเลขเท่านั้น
        elif not account_number.isdigit():
            error_message = "กรุณากรอกเลขบัญชีที่ถูกต้อง"
        # ตรวจสอบความซ้ำซ้อน
        elif PaymentMethod.objects.filter(
                restaurant_profile=restaurant_profile,
                bank_name=bank_name,
                account_number=account_number).exists():
            error_message = "บัญชีนี้มีอยู่แล้ว"
        else:
            # บันทึกข้อมูลเมื่อผ่าน Validation ทั้งหมด
            PaymentMethod.objects.create(
                restaurant_profile=restaurant_profile,
                bank_name=bank_name,
                account_number=account_number
            )
            return redirect('restaurant:edit_menu_payment')

    payment_methods = PaymentMethod.objects.filter(restaurant_profile=restaurant_profile)
    return render(request, "add_payment.html", {
        'payment_methods': payment_methods,
        'error_message': error_message
    })
    
def edit_only_payment(request):
    username = request.user.username
    restaurant = get_object_or_404(RestaurantProfile, user_profile__user__username=username)
    is_editing = request.GET.get("edit")

    payment_id = None
    payment_item = None

    if request.method == "POST":
        payment_id = request.POST.get("payment_id")
        if payment_id:
            payment_item = get_object_or_404(PaymentMethod, id=payment_id)
            if request.POST.get('delete_payment_method') == 'true':
                payment_item.delete()
                return redirect('restaurant:edit_menu_payment')
            if "bank_name" in request.POST:
                bank_name = request.POST.get("bank_name").strip()
                payment_item.bank_name = bank_name
            elif "account_number" in request.POST:
                account_number = request.POST.get("account_number", "").strip()
                payment_item.account_number = account_number
            payment_item.save()

            return render(request, "edit_only_payment.html", {"restaurant": restaurant, "payment_item": payment_item, "payment_id": payment_id})

    elif request.method == "GET":
        payment_id = request.GET.get("payment_id")
        if payment_id:
            payment_item = get_object_or_404(PaymentMethod, id=payment_id)
    
    

    return render(
        request,
        "edit_only_payment.html",
        {
            "restaurant": restaurant,
            "payment_item": payment_item,
            "payment_id": payment_id,
            "is_editing": is_editing,
        },
    )
    
