from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from .models import UserProfile
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

def index(request):      
    return render(request, "index.html")

def kinkorn(request):      
    return render(request, "index.html")

def about(request):
    if request.method == "POST":
        return HttpResponseRedirect("about")      
    return render(request, "about.html")

def order(request):      
    return render(request, "index.html")

def yourorder(request):      
    return render(request, "index.html")

def index_restaurant(request):
    if request.method == "POST":
        return HttpResponseRedirect("index_restaurant")   
    return render(request, "index_restaurant.html")


def choose_regis(request):
    if request.method == "POST":
        user_type = request.POST.get("user_type")  
        request.session['user_type'] = user_type  
        return redirect("register") 
    return render(request, "choose_regis.html")


# ฟังก์ชันสำหรับการลงทะเบียน

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

    
        user = User.objects.create_user(username=username, password=password, email=email)
        # สร้าง UserProfile ที่เชื่อมโยงกับ User ที่สร้างขึ้น
        profile = UserProfile.objects.create(
            user=user, 
            phone_number=phone_number, 
            user_type=user_type
        )

        messages.success(request, "ลงทะเบียนสำเร็จ!")
        login(request, user)
        return redirect("login") 

    # ส่ง user_type ไปยังหน้า register.html
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
                return redirect("index_restaurant")  
            else:
                return redirect("index") 

            messages.success(request, "เข้าสู่ระบบสำเร็จ!")
            return redirect("index")  # หากไม่มี user_type ก็ให้ไปหน้า index

        else:
            messages.error(request, "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")

    return render(request, "login.html")
