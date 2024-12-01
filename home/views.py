from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.urls import reverse
from .models import UserProfile, RestaurantProfile, Menu, Order
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required


def index(request):      
    return render(request, "index.html")

def kinkorn(request):      
    return render(request, "index.html")

def about(request):   
    return render(request, "about.html")

def order(request):      
    return render(request, "index.html")

def yourorder(request):      
    return render(request, "index.html")


def welcome_registration(request): 
    user_type = request.GET.get('user_type', 'default_value') 
    username = request.GET.get('username', 'default_value')
    restaurant_name= request.GET.get('restaurant_name', 'default_value')

    context = {
        'user_type': user_type,
        'username': username,
        'restaurant_name': restaurant_name,
    }
    
    return render(request, "welcome_registration.html", context)



def choose_regis(request):
    if request.method == "POST":
        user_type = request.POST.get("user_type")  
        request.session['user_type'] = user_type  
        if user_type == 'restaurant':
            return redirect("register") 
        else:
            return redirect("customer_register")            
            
    return render(request, "choose_regis.html")

def customer_register(request):
    return render(request, "customer_register.html")

def restaurant_register(request):
    username = request.user.username  # รับ username จาก query parameter
    user_profile = UserProfile.objects.get(user=request.user)
    food_categories = RestaurantProfile.Foodcate.choices

    if request.method == "POST":
        '''
        if "back" in request.POST:
            return redirect("register")
        '''
        restaurant_name = request.POST.get("restaurant_name")
        food_category = request.POST.get("food_category")
        about = request.POST.get("about")
        open_close_time = request.POST.get("open_close_time")

        # รับไฟล์รูปภาพจากฟอร์ม
        if 'restaurant_picture' in request.FILES:
            restaurant_picture = request.FILES['restaurant_picture']
            fs = FileSystemStorage()
            filename = fs.save(restaurant_picture.name, restaurant_picture)  # บันทึกไฟล์
            restaurant_picture_url = fs.url(filename)  # ดึง URL ของไฟล์ที่บันทึก

        else:
            restaurant_picture_url = None

        restaurant_info = RestaurantProfile.objects.create(
            user_profile=user_profile,
            restaurant_name=restaurant_name, 
            food_category=food_category, 
            about=about,
            open_close_time=open_close_time,
            restaurant_picture=restaurant_picture 
        )
        restaurant_info.save()
        
        url = reverse("add_menu")
        return redirect(f"{url}?restaurant_name={restaurant_name}")

    return render(request, "restaurant_register.html", {"username": username,'food_categories': food_categories})

def add_menu(request):
    restaurant_name = request.GET.get('restaurant_name', 'default_restaurant_name')
    food_categories = RestaurantProfile.Foodcate.choices

    if request.method == "POST":
        food_name = request.POST.get("food_name")
        food_category = request.POST.get("food_category")
        about = request.POST.get("about")
        price = request.POST.get("price")
        user_type = request.POST.get("user_type")

        # ค้นหา RestaurantProfile
        restaurant_profile = get_object_or_404(RestaurantProfile, restaurant_name=restaurant_name)

        # รับไฟล์รูปภาพจากฟอร์มและบันทึกใน menu_picture
        menu_picture = None  # ตั้งค่าเริ่มต้น
        if 'menu_picture' in request.FILES:
            menu_picture = request.FILES['menu_picture']

        # สร้างข้อมูลเมนูและบันทึกข้อมูล
        food_info = Menu.objects.create(
            restaurant_profile=restaurant_profile,
            food_name=food_name, 
            food_category=food_category, 
            about=about,
            menu_picture=menu_picture,  # บันทึกใน menu_picture
            price=price
        )
        food_info.save()

        url = reverse("welcome_registration")
        return redirect(f"{url}?user_type=restaurant&restaurant_name={restaurant_name}")     

    return render(request, "add_menu.html", {"restaurant_name": restaurant_name, 'food_categories': food_categories})

    

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        phone_number = request.POST.get("phone_number")
        email = request.POST.get("email")
        user_type = request.POST.get("user_type")

        # หากไม่มีการเลือก user_type, กำหนดค่า default จาก query parameter
        if not user_type:
            user_type = request.GET.get("user_type", "customer")  

        # ตรวจสอบว่าชื่อผู้ใช้มีอยู่แล้วในระบบหรือไม่
        if User.objects.filter(username=username).exists():
            messages.error(request, "ชื่อผู้ใช้นี้มีอยู่แล้วในระบบ")
            return render(request, "register.html", {"user_type": user_type})

        profile_picture = request.FILES.get("profile_picture", None)
    
        user = User.objects.create_user(username=username, password=password, email=email)
        profile = UserProfile.objects.create(
            user=user, 
            phone_number=phone_number, 
            user_type=user_type
        )
        
        if profile_picture:
            profile.profile_picture = profile_picture
            profile.save()

        messages.success(request, "ลงทะเบียนสำเร็จ!")
        login(request, user)
        if user_type == "restaurant":
            return redirect("restaurant_register")
        else:
            url = reverse("welcome_registration")
            return redirect(f"{url}?user_type=customer&username={username}")

    user_type = request.GET.get("user_type", "customer")
    return render(request, "register.html", {"user_type": user_type})



# ตรวจสอบการเข้าสู่ระบบ
def authenticate_user_profile(username, password):
    try:
        user = UserProfile.objects.get(username=username)
        # ตรวจสอบรหัสผ่าน
        if check_password(password, user.password):  # ใช้ check_password เพื่อเช็คการเข้ารหัส
            return user
        else:
            return None
    except UserProfile.DoesNotExist:
        return None


# ฟังก์ชันสำหรับการเข้าสู่ระบบ
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # ใช้ฟังก์ชัน authenticate เพื่อตรวจสอบชื่อผู้ใช้และรหัสผ่าน
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  
            
            try:
                profile = UserProfile.objects.get(user=user)
                user_type = profile.user_type
            except UserProfile.DoesNotExist:
                user_type = None

            if user_type == "restaurant":
                return redirect("/restaurant/")  
            else:
                return redirect("/order/") 

            messages.success(request, "เข้าสู่ระบบสำเร็จ!")
            return redirect("index")  # หากไม่มี user_type ก็ให้ไปหน้า index

        else:
            messages.error(request, "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")

    return render(request, "login.html")


def logout_view(request):
    logout(request)  # ล็อกเอาท์ผู้ใช้
    return redirect('/')  # เปลี่ยนเส้นทางไปที่หน้าแรกหลังจากออกจากระบบ

def restaurant_list(request):
    restaurants = RestaurantProfile.objects.all()  # ดึงข้อมูลร้านอาหารทั้งหมด
    return render(request, 'order.html', {'restaurants': restaurants})

def menu_list(request, restaurant_id):
    restaurant = get_object_or_404(RestaurantProfile, id=restaurant_id)
    menu_items = Menu.objects.filter(restaurant_profile=restaurant)
    return render(request, 'menu_list.html', {'restaurant': restaurant, 'menu_items': menu_items})


from django.contrib.auth.decorators import login_required

@login_required
def your_order(request):
    # กรองออเดอร์ของผู้ใช้
    orders = Order.objects.filter(user_profile=request.user.userprofile)

    # คำนวณจำนวนเงินทั้งหมด
    total_amount = sum(order.total_price for order in orders)

    # สร้าง Dictionary เพื่อจัดกลุ่มออเดอร์ตามร้าน
    restaurant_orders = {}
    for order in orders:
        restaurant_name = order.menu.restaurant_profile.restaurant_name
        if restaurant_name not in restaurant_orders:
            restaurant_orders[restaurant_name] = {
                'orders': [],
                'delivery_option': order.delivery_option  # กำหนดค่า delivery_option ที่เลือกล่าสุด
            }
        restaurant_orders[restaurant_name]['orders'].append(order)

    return render(request, "your_order.html", {
        "restaurant_orders": restaurant_orders,
        "total_amount": total_amount,
    })



@login_required
def update_order_quantity(request, order_id):
    order = get_object_or_404(Order, id=order_id, user_profile=request.user.userprofile)

    # ตรวจสอบว่าผู้ใช้ต้องการเพิ่มหรือลดจำนวน
    action = request.POST.get('action')

    if action == 'increase':
        order.quantity += 1  # เพิ่มจำนวนอาหาร
    elif action == 'decrease' and order.quantity > 1:
        order.quantity -= 1  # ลดจำนวนอาหาร (ไม่ให้ลดต่ำกว่า 1)

    # คำนวณราคาใหม่
    order.total_price = order.quantity * order.menu.price
    order.save()

    return redirect('your_order')  # รีเฟรชหน้าเพื่อแสดงการอัพเดต

@login_required
def update_delivery_option(request):
    user_profile = request.user.userprofile  # ตรวจสอบว่า user มี profile หรือไม่
    delivery_option = request.POST.get('delivery_option')  # รับค่าจากฟอร์ม

    # กรองออเดอร์ตาม user_profile
    orders = Order.objects.filter(user_profile=user_profile)

    # อัพเดตตัวเลือกการรับอาหาร
    for order in orders:
        order.delivery_option = delivery_option
        order.save()

    return redirect("your_order")  # รีเฟรชหน้าเพื่อแสดงการอัพเดต

        
@login_required
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user_profile=request.user.userprofile)
    order.delete()
    return redirect("your_order")

@login_required
def upload_payment_slip(request, order_id):
    order = Order.objects.get(id=order_id)

    if request.method == 'POST' and request.FILES.get('payment_slip'):
        # เก็บสลิปการชำระเงิน
        order.payment_slip = request.FILES['payment_slip']
        order.status = 'paid'  # เปลี่ยนสถานะเป็น 'paid'
        order.save()

        # ตรวจสอบว่าออเดอร์ทุกตัวในร้านถูกชำระเงินแล้วหรือไม่
        restaurant_orders = Order.objects.filter(restaurant_profile=order.restaurant_profile, status='paid')
        if restaurant_orders.count() == Order.objects.filter(restaurant_profile=order.restaurant_profile).count():
            for o in restaurant_orders:
                o.status = 'paid'
                o.save()

        return redirect('order_status')

    return render(request, 'upload_payment_slip.html', {'order': order})


@login_required
def confirm_order(request):
    if not request.user.is_authenticated:
        return redirect('login')

    # ค้นหาทุกออเดอร์ของผู้ใช้ที่ยังไม่ถูกยืนยันการชำระเงิน
    orders = Order.objects.filter(user_profile=request.user.userprofile, status='pending')

    for order in orders:
        # เปลี่ยนสถานะของออเดอร์เป็น 'waiting_for_payment'
        order.status = 'waiting_for_payment'
        order.save()

    # รีไดเรกต์ไปยังหน้าสถานะ
    return redirect('order_status')

def order_status(request):
    # ดึงข้อมูลออเดอร์ที่เกี่ยวข้องกับผู้ใช้
    orders = Order.objects.filter(user_profile=request.user.userprofile)
    
    # สร้าง Dictionary สำหรับเก็บออเดอร์ที่ถูกจัดกลุ่มตามร้าน
    restaurant_orders = {}
    for order in orders:
        restaurant_name = order.menu.restaurant_profile.restaurant_name
        if restaurant_name not in restaurant_orders:
            restaurant_orders[restaurant_name] = []
        restaurant_orders[restaurant_name].append(order)
    
    # คำนวณ total_price สำหรับแต่ละร้าน
    for restaurant_name, orders_list in restaurant_orders.items():
        total_price = sum(order.total_price for order in orders_list)
        # ส่ง total_price ไปยัง template
        restaurant_orders[restaurant_name] = {'orders': orders_list, 'total_price': total_price}
    
    return render(request, "order_status.html", {
        "orders": orders,
        "restaurant_orders": restaurant_orders,
    })

def add_to_order(request, menu_id):

    menu = Menu.objects.get(id=menu_id)
    

    quantity = int(request.POST.get('quantity', 1))  
    delivery_option = request.POST.get('delivery_option', 'in_store') 

    if request.user.is_authenticated:
        user_profile = request.user.userprofile 
       
        total_price = menu.price * quantity


        order = Order.objects.create(
            user_profile=user_profile,
            menu=menu,
            quantity=quantity,
            total_price=total_price,
            delivery_option=delivery_option
        )

        return redirect('your_order')  
    else:
        return redirect('login')  