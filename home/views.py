from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.urls import reverse
from .models import UserProfile, RestaurantProfile, Menu, Order, OrderItem
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.utils import timezone  # เพิ่มการ import timezone

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
        name = request.POST.get("name")
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
            name=name,
            email=email, 
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

@login_required
def your_order(request):
    # ดึงคำสั่งซื้อที่รอการชำระเงิน
    restaurant = RestaurantProfile.objects.first()  
    order = Order.objects.filter(user_profile=request.user.userprofile, status='waiting_for_payment').first()

    if not order:
        # ถ้าไม่พบคำสั่งซื้อที่มีสถานะ 'waiting_for_payment' ให้สร้างคำสั่งซื้อใหม่
        order = Order.objects.create(
            user_profile=request.user.userprofile,
            status='waiting_for_payment',  # กำหนดสถานะเริ่มต้น
            total_price=0,  # ราคาเริ่มต้น
            pickup_time=None,  # เวลารับสามารถเพิ่มเติมได้
            restaurant=restaurant  # กำหนดร้านอาหาร
        )

    if request.method == 'POST':
        if 'save_order' in request.POST:  # ถ้าผู้ใช้กดบันทึกการเลือก
            pickup_time = request.POST.get('pickup_time')
            delivery_option = request.POST.get('delivery_option')
            
            # อัพเดทคำสั่งซื้อ
            order.pickup_time = pickup_time
            order.delivery_option = delivery_option
            order.save()
            
            return redirect('your_order')  # ไปที่หน้ารายการคำสั่งซื้อ

        else:  # ถ้าผู้ใช้เพิ่มเมนูในคำสั่งซื้อ
            menu_id = request.POST.get('menu_id')
            if menu_id:
                try:
                    menu = Menu.objects.get(id=menu_id)
                    existing_item = order.order_items.filter(restaurant_menu=menu).first()
                    if existing_item:
                        existing_item.quantity += 1
                        existing_item.total_price = existing_item.restaurant_menu.price * existing_item.quantity
                        existing_item.save()
                    else:
                        OrderItem.objects.create(
                            order=order,
                            restaurant_menu=menu,
                            quantity=1,
                            total_price=menu.price
                        )
                    
                    # คำนวณราคาทั้งหมด
                    total_price = sum(item.total_price for item in order.order_items.all())
                    order.total_price = total_price
                    order.save()

                except Menu.DoesNotExist:
                    pass

            return redirect('your_order')  # รีเฟรชหน้า

    # หากไม่ใช่ POST ให้แสดงข้อมูลคำสั่งซื้อ
    return render(request, 'your_order.html', {'order': order})

@login_required
def order_status(request):
    orders = Order.objects.filter(user_profile=request.user.userprofile)

    return render(request, "order_status.html", {"orders": orders})

@login_required
def upload_payment_slip(request, order_id):
    # ดึงออเดอร์ที่เราต้องการ
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST' and 'payment_slip' in request.FILES:
        payment_slip = request.FILES['payment_slip']
        order.payment_slip = payment_slip
        order.status = 'paid' 
        order.save() 
        messages.success(request, "ชำระเงินเรียบร้อยแล้ว")
    
    return redirect('order_status')


@login_required
def order_confirmation(request):
    # ดึงออร์เดอร์ที่ผู้ใช้กำลังทำการยืนยัน
    order = Order.objects.get(id=request.POST.get('order_id'), user_profile=request.user.userprofile)

    # เปลี่ยนสถานะออร์เดอร์เมื่อยืนยัน
    order.status = 'paid'  # หรือ 'completed' ขึ้นอยู่กับขั้นตอน
    order.save()

    # กลับไปยังหน้าแสดงสถานะออร์เดอร์
    return redirect('order_status')

@login_required
def order_status(request):
    orders = Order.objects.filter(user_profile=request.user.userprofile)
    return render(request, "order_status.html", {"orders": orders})


