from django.test import Client, TestCase
from django.test import TestCase
from django.urls import reverse
from restaurant.models import RestaurantProfile
from django.contrib.auth.models import User
from restaurant.models import UserProfile, RestaurantProfile, Menu,  PaymentMethod
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



       
class ManageViewTest(TestCase):
    #สร้างข้อมูล user ให้เชื่อมกับ UserProfileและสร้างข้อมูลร้านอาหาร
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
        

        
class EditMenuPaymentTest(TestCase):
    #สร้างข้อมูล user ให้เชื่อมกับ UserProfilecและสร้างข้อมูลร้านอาหารและเมนู
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            user_type="restaurant",
            name="Test User"
        )
        self.restaurant = RestaurantProfile.objects.create(
            user_profile=self.user_profile,
            restaurant_name="Test Restaurant",
            about="This is a test restaurant",
            open_close_time="09:00-20:00"
        )
        self.menu1 = Menu.objects.create(
            restaurant_profile=self.restaurant,
            food_name="Test Food 1",
            about="Delicious test food",
            price=50.00
        )
        self.menu2 = Menu.objects.create(
            restaurant_profile=self.restaurant,
            food_name="Test Food 2",
            about="Yummy test food",
            price=100.00
        )


        self.client.login(username="testuser", password="password")

    def test_edit_menu_payment_view(self):
        response = self.client.get(reverse('restaurant:edit_menu_payment'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_menu_payment.html')
        self.assertEqual(response.context['restaurant'], self.restaurant)
        
        menu_items = response.context['menu_items']
        self.assertIn(self.menu1, menu_items)
        self.assertIn(self.menu2, menu_items)


        self.assertContains(response, "Test Restaurant")  
        self.assertContains(response, "Test Food 1")      
        self.assertContains(response, "Test Food 2")


class AddMenuResTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            user_type="restaurant",
            name="Test User"
        )

        self.restaurant = RestaurantProfile.objects.create(
            user_profile=self.user_profile,
            restaurant_name="Test Restaurant",
            about="This is a test restaurant",
            open_close_time="09:00-20:00"
        )
  
        self.client.login(username="testuser", password="password")

    def test_add_menu_res_get(self):
        response = self.client.get(reverse('restaurant:add_menu_res'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_menu_res.html')
        self.assertEqual(response.context['restaurant_name'], self.restaurant.restaurant_name)


class EditOnlyMenuTest(TestCase):
    def setUp(self):
        # สร้างข้อมูลผู้ใช้และร้านอาหาร
        self.user = User.objects.create_user(username="testuser", password="password")
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            user_type="restaurant",
            name="Test User"
        )
        self.restaurant = RestaurantProfile.objects.create(
            user_profile=self.user_profile,
            restaurant_name="Test Restaurant",
            food_category="ข้าวราดแกง",
            about="This is a test restaurant",
            open_close_time="09:00-20:00"
        )
        # สร้างข้อมูลเมนู
        self.menu_item = Menu.objects.create(
            restaurant_profile=self.restaurant,
            food_name="Test Food",
            about="Delicious test food",
            price=50.00
        )
        # ล็อกอินผู้ใช้
        self.client.login(username="testuser", password="password")

    # ทดสอบการเข้าถึง view
    def test_edit_only_menu_view_access(self):
        response = self.client.get(reverse("restaurant:edit_only_menu"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "edit_only_menu.html")
        self.assertEqual(response.context["restaurant"], self.restaurant)

    # ทดสอบการแก้ไขชื่ออาหาร 
    def test_edit_only_menu_post_valid(self):
        response = self.client.post(reverse("restaurant:edit_only_menu"), {
            "menu_id": self.menu_item.id,
            "food_name": "Updated Food Name"
        })
        self.assertEqual(response.status_code, 200)
        self.menu_item.refresh_from_db()
        self.assertEqual(self.menu_item.food_name, "Updated Food Name")
        self.assertContains(response, "Updated Food Name")

    # ทดสอบการส่งข้อมูลโดยไม่มี food_name 
    def test_edit_only_menu_post_no_food_name(self):
        response = self.client.post(reverse("restaurant:edit_only_menu"), {
            "menu_id": self.menu_item.id
        })
        self.assertEqual(response.status_code, 200)  
        self.menu_item.refresh_from_db()
        self.assertNotEqual(self.menu_item.food_name, "")  

    # ทดสอบ context ว่ามีข้อมูล food_categories และ is_editing หรือไม่
    def test_edit_only_menu_context(self):
        response = self.client.get(reverse("restaurant:edit_only_menu"))
        self.assertIn("food_categories", response.context)
        self.assertIn("is_editing", response.context)

class AddPaymentTest(TestCase):
    def setUp(self):
        # สร้างข้อมูลผู้ใช้และร้านอาหาร
        self.user = User.objects.create_user(username="testuser", password="password")
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            user_type="restaurant",
            name="Test User"
        )
        self.restaurant = RestaurantProfile.objects.create(
            user_profile=self.user_profile,
            restaurant_name="Test Restaurant",
            about="This is a test restaurant",
            open_close_time="09:00-20:00"
        )
        # ล็อกอินผู้ใช้
        self.client.login(username="testuser", password="password")

    # ทดสอบการเข้าถึงหน้าเพิ่มช่องทางการชำระเงิน
    def test_add_payment_view_access(self):
        response = self.client.get(reverse("restaurant:add_payment"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "add_payment.html")
        self.assertIn("payment_methods", response.context)
        self.assertIn("error_message", response.context)

    # ทดสอบการเพิ่มช่องทางการชำระเงิน 
    def test_add_payment_post_valid(self):
        response = self.client.post(reverse("restaurant:add_payment"), {
            "bank_name": "Test Bank",
            "account_number": "1234567890"
        })
        self.assertEqual(response.status_code, 302)  
        payment_methods = PaymentMethod.objects.filter(restaurant_profile=self.restaurant)
        self.assertEqual(payment_methods.count(), 1)
        self.assertEqual(payment_methods.first().bank_name, "Test Bank")
        self.assertEqual(payment_methods.first().account_number, "1234567890")

    