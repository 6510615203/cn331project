from django.test import Client, TestCase
from django.test import TestCase
from django.urls import reverse
from restaurant.models import RestaurantProfile
from django.contrib.auth.models import User
from .models import RestaurantProfile, Menu
from home.models import UserProfile  
from django.core.files.uploadedfile import SimpleUploadedFile

class GeneralViewTest(TestCase):
    #สร้างข้อมูล user ให้เชื่อมกับ UserProfilecและสร้างข้อมูลร้านอาหาร
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user_profile = UserProfile.objects.create(user=self.user)
        self.restaurant = RestaurantProfile.objects.create(
            user_profile=self.user_profile,
            restaurant_name='Test Restaurant',
            food_category='ข้าวราดแกง',
            about='A test restaurant',
            open_close_time='10:00-22:00',
        )
        
    #ลองล้อกอิน + ส่งคำขอ http ไป view ให้ตรวจสอบสถานะ http ,template กับ ข้อมูลไปว่าตรงกับที่เราเซ็ตไหม"
    def test_index(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('restaurant:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index_restaurant.html')
        self.assertEqual(response.context['restaurant'], self.restaurant)
        
    #ส่งคำขอ http ไป view ให้ตรวจสอบสถานะ http ,template กับ ข้อมูลไปว่าตรงกับที่เราเซ็ตไหม"    
    def test_about_view(self):
        response = self.client.get(reverse('restaurant:about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "about_kinkorn.html")

    def test_order_list_view(self):
        response = self.client.get(reverse('restaurant:order_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "order_list.html")

    def test_sales_report_view(self):
        response = self.client.get(reverse('restaurant:sales_report'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "sales.html")

    def test_add_payment_view(self):
        response = self.client.get(reverse('restaurant:add_payment'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "add_payment.html")

        
class ManageViewTest(TestCase):
    #สร้างข้อมูล user ให้เชื่อมกับ UserProfilecและสร้างข้อมูลร้านอาหาร
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user_profile = UserProfile.objects.create(user=self.user)
        self.restaurant = RestaurantProfile.objects.create(
            user_profile=self.user_profile,
            restaurant_name='ทูซิท',
            food_category='น้ำ',
            about='A test restaurant',
            open_close_time='10:00-22:00',
        )
        
    #ส่งคำขอ http ไป view พร้อมกับข้อมูล และดึงข้อมูลล่าสุดมาตรวจสอบว่าตรงกันไหม
    def test_update_restaurant_name(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse("restaurant:manage"), 
            {" restaurant_name": "หิวสหาย"}
        )
        self.restaurant.refresh_from_db()
        self.assertEqual(self.restaurant.restaurant_name, "หิวสหาย")

    def test_update_food_category(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse("restaurant:manage"), 
            {"food_category": "อาหารญี่ปุ่น"}
        )
        self.restaurant.refresh_from_db()
        self.assertEqual(self.restaurant.food_category, "อาหารญี่ปุ่น")

    def test_update_about(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse("restaurant:manage"), 
            {"about": "Updated about information"}
        )
        self.restaurant.refresh_from_db()
        self.assertEqual(self.restaurant.about, "Updated about information")

    def test_update_open_close_time(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse("restaurant:manage"), 
            {"open_close_time": "09:00-20:00"}
        )
        self.restaurant.refresh_from_db()
        self.assertEqual(self.restaurant.open_close_time, "09:00-20:00")

    #สร้างไฟล์ภาพรูปแบบไบต์ ส่งคำขอ http ไป view ไฟล์ภาพถูกอัปโหลด restaurant_picture จะมีค่า
    def test_update_restaurant_picture(self):
        self.client.login(username="testuser", password="testpassword")
        test_image = SimpleUploadedFile(
            "test_image.jpg",
            b"fake_image_content", 
            content_type="image/jpeg"
        )
        response = self.client.post(
            reverse("restaurant:manage"),
            {"restaurant_picture": test_image},
        )
        self.restaurant.refresh_from_db()
        self.assertTrue(self.restaurant.restaurant_picture)
        



    
