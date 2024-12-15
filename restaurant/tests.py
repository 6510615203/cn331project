import os
from django.test import Client, TestCase
from django.test import TestCase
from django.urls import reverse
from restaurant.models import RestaurantProfile
from django.contrib.auth.models import User
from restaurant.models import UserProfile, RestaurantProfile, PaymentMethod
from home.models import UserProfile,Order,Menu
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import datetime, timedelta

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
        # สร้าง User
        self.user = User.objects.create_user(username="testuser", password="password123")

        # สร้าง UserProfile (ถ้ามี)
        self.user_profile = UserProfile.objects.create(user=self.user)

        # สร้าง RestaurantProfile
        self.restaurant_profile = RestaurantProfile.objects.create(user_profile=self.user_profile)

        # สร้าง PaymentMethod
        self.payment_method = PaymentMethod.objects.create(
            bank_name="Test Bank",
            account_number="123456789",
            restaurant=self.restaurant_profile
        )
        # ล็อกอินผู้ใช้
        self.client.login(username="testuser", password="password")

    # ทดสอบการเข้าถึง view
    def test_edit_only_menu_view_access(self):
        response = self.client.get(reverse("restaurant:edit_only_menu"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "edit_only_menu.html")
        self.assertEqual(response.context["restaurant"], self.restaurant)


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

class OrderListViewTest(TestCase):
    def setUp(self):
        # สร้างผู้ใช้และโปรไฟล์ร้านอาหาร
        self.user = User.objects.create_user(username='restaurant_user', password='password123')
        self.user_profile = UserProfile.objects.create(user=self.user, user_type='restaurant')
        self.restaurant = RestaurantProfile.objects.create(user_profile=self.user_profile, restaurant_name='Test Restaurant')
        
        # สร้างคำสั่งซื้อ
        self.order = Order.objects.create(
            user_profile=self.user_profile,
            restaurant=self.restaurant,
            total_price=100.00,
            status='waiting_for_payment'
        )

    def test_confirm_payment(self):
        self.client.login(username='restaurant_user', password='password123')
        
        response = self.client.post(reverse('restaurant:order_list'), {
            'order_id': self.order.id,
            'action': 'confirm_payment'
        })

        self.order.refresh_from_db()  # อัปเดตข้อมูลจากฐานข้อมูล
        self.assertEqual(self.order.status, 'paid')
        self.assertRedirects(response, reverse('restaurant:order_list'))

    def test_mark_in_progress(self):
        self.order.status = 'paid'
        self.order.save()

        self.client.login(username='restaurant_user', password='password123')

        response = self.client.post(reverse('restaurant:order_list'), {
            'order_id': self.order.id,
            'action': 'mark_in_progress'
        })

        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'cooking')
        self.assertRedirects(response, reverse('restaurant:order_list'))

    def test_mark_completed(self):
        self.order.status = 'cooking'
        self.order.save()

        self.client.login(username='restaurant_user', password='password123')

        response = self.client.post(reverse('restaurant:order_list'), {
            'order_id': self.order.id,
            'action': 'mark_completed'
        })

        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'completed')
        self.assertRedirects(response, reverse('restaurant:order_list'))

class AddMenuTest(TestCase):
    def setUp(self):
        # สร้างผู้ใช้งาน
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.user_profile = UserProfile.objects.create(user=self.user, user_type="restaurant")
        self.restaurant = RestaurantProfile.objects.create(
            user_profile=self.user_profile,
            restaurant_name="Test Restaurant",
            food_category="ข้าวราดแกง",
        )
        self.client = Client()

    def test_add_menu_get(self):
        """ทดสอบการโหลดหน้าเพิ่มเมนู (GET)"""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("restaurant:add_menu_res"))
        self.assertEqual(response.status_code, 200)  # ตรวจสอบว่าโหลดสำเร็จ
        self.assertTemplateUsed(response, "add_menu_res.html")  # ตรวจสอบ Template
        self.assertIn("food_categories", response.context)  # ตรวจสอบว่า context มี `food_categories`

    def test_add_menu_post(self):
        """ทดสอบการเพิ่มเมนูใหม่ (POST)"""
        self.client.login(username="testuser", password="testpassword")
        # สร้างรูปภาพจำลอง
        image_file = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        post_data = {
            "food_name": "Test Food",
            "food_category": "ข้าวราดแกง",
            "about": "Delicious Test Food",
            "price": "50.00",
            "menu_picture": image_file,
        }
        response = self.client.post(reverse("restaurant:add_menu_res"), post_data)

        # ตรวจสอบว่ามีการ redirect หลังจากการเพิ่มเมนู
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('restaurant:edit_menu_payment')}?user_type=restaurant&restaurant_name=Test%20Restaurant")

        # ตรวจสอบว่ามีการสร้างเมนูในฐานข้อมูล
        self.assertEqual(Menu.objects.count(), 1)
        menu = Menu.objects.first()
        self.assertEqual(menu.food_name, "Test Food")
        self.assertEqual(menu.food_category, "ข้าวราดแกง")
        self.assertEqual(menu.about, "Delicious Test Food")
        self.assertEqual(menu.price, 50.00)
        self.assertIn("test_image", menu.menu_picture.name)


    def test_add_menu_post_no_picture(self):
        """ทดสอบการเพิ่มเมนูใหม่โดยไม่มีรูปภาพ (POST)"""
        self.client.login(username="testuser", password="testpassword")
        post_data = {
            "food_name": "Test Food Without Picture",
            "food_category": "ข้าวราดแกง",
            "about": "Delicious Food Without Picture",
            "price": "60.00",
        }
        response = self.client.post(reverse("restaurant:add_menu_res"), post_data)

        # ตรวจสอบว่ามีการ redirect หลังจากการเพิ่มเมนู
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('restaurant:edit_menu_payment')}?user_type=restaurant&restaurant_name=Test%20Restaurant")

        # ตรวจสอบว่ามีการสร้างเมนูในฐานข้อมูล
        self.assertEqual(Menu.objects.count(), 1)
        menu = Menu.objects.first()
        self.assertEqual(menu.food_name, "Test Food Without Picture")
        self.assertFalse(menu.menu_picture)  


class AddPaymentTest(TestCase):
    def setUp(self):
        # สร้างผู้ใช้และร้านอาหารสำหรับทดสอบ
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.user_profile = UserProfile.objects.create(user=self.user, user_type="restaurant")
        self.restaurant_profile = RestaurantProfile.objects.create(
            user_profile=self.user_profile,
            restaurant_name="Test Restaurant"
        )
        self.add_payment_url = reverse('restaurant:add_payment')

    def test_add_payment_view_get(self):
        """ทดสอบการเรียกดูหน้า add_payment"""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(self.add_payment_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "add_payment.html")

    def test_add_payment_successful_post(self):
        """ทดสอบการเพิ่มข้อมูลการชำระเงินสำเร็จ"""
        self.client.login(username="testuser", password="testpassword")
        post_data = {
            "bank_name": "Test Bank",
            "account_number": "123456789",
        }
        response = self.client.post(self.add_payment_url, post_data)
        self.assertEqual(PaymentMethod.objects.count(), 1)
        payment = PaymentMethod.objects.first()
        self.assertEqual(payment.bank_name, "Test Bank")
        self.assertEqual(payment.account_number, "123456789")
        self.assertEqual(payment.restaurant_profile, self.restaurant_profile)
        self.assertRedirects(response, reverse('restaurant:edit_menu_payment'))

class EditOnlyMenuViewTest(TestCase):
    def setUp(self):
        # สร้างข้อมูลทดสอบ User, UserProfile, RestaurantProfile, และ Menu
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user_profile = UserProfile.objects.create(user=self.user, user_type='restaurant')
        self.restaurant = RestaurantProfile.objects.create(
            user_profile=self.user_profile,
            restaurant_name="Test Restaurant",
        )
        self.menu = Menu.objects.create(
            restaurant_profile=self.restaurant,
            food_name="Test Menu",
            about="Test About",
            price=100.00,
        )

    def test_get_menu_for_edit(self):
        # ทดสอบการดึงข้อมูลเมนูเพื่อแก้ไข
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('restaurant:edit_only_menu') + f'?menu_id={self.menu.id}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_only_menu.html')
        self.assertEqual(response.context['menu_item'], self.menu)

    def test_update_menu_name(self):
        # ทดสอบการแก้ไขชื่อเมนู
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('restaurant:edit_only_menu'), {
            'menu_id': self.menu.id,
            'food_name': 'Updated Menu Name'
        })
        self.assertEqual(response.status_code, 200)
        self.menu.refresh_from_db()
        self.assertEqual(self.menu.food_name, 'Updated Menu Name')

    def test_delete_menu(self):
        # ทดสอบการลบเมนู
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('restaurant:edit_only_menu'), {
            'menu_id': self.menu.id,
            'delete_menu': 'true'
        })
        self.assertEqual(response.status_code, 302)  # Redirect หลังลบสำเร็จ
        self.assertFalse(Menu.objects.filter(id=self.menu.id).exists())


class EditOnlyMenuTest(TestCase):
    def setUp(self):
        # สร้างผู้ใช้และข้อมูลที่เกี่ยวข้อง
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.user_profile = UserProfile.objects.create(user=self.user, user_type="restaurant")
        self.restaurant = RestaurantProfile.objects.create(
            user_profile=self.user_profile,
            restaurant_name="Test Restaurant",
        )
        self.menu = Menu.objects.create(
            restaurant_profile=self.restaurant,
            food_name="Test Menu",
            food_category="ข้าวราดแกง",
            about="Test About",
            price=100.00,
        )

        # ล็อกอินผู้ใช้
        self.client.login(username="testuser", password="testpassword")

    def test_get_menu_item(self):
        """ทดสอบการดึงข้อมูลเมนูผ่าน GET"""
        response = self.client.get(reverse("restaurant:edit_only_menu") + f"?menu_id={self.menu.id}")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "edit_only_menu.html")
        self.assertEqual(response.context["menu_item"], self.menu)

    def test_update_food_name(self):
        """ทดสอบการแก้ไขชื่อเมนู"""
        response = self.client.post(reverse("restaurant:edit_only_menu"), {
            "menu_id": self.menu.id,
            "food_name": "Updated Menu Name",
        })
        self.menu.refresh_from_db()
        self.assertEqual(self.menu.food_name, "Updated Menu Name")

    def test_update_food_category(self):
        """ทดสอบการแก้ไขประเภทเมนู"""
        response = self.client.post(reverse("restaurant:edit_only_menu"), {
            "menu_id": self.menu.id,
            "food_category": "ก๋วยเตี๋ยว",
        })
        self.menu.refresh_from_db()
        self.assertEqual(self.menu.food_category, "ก๋วยเตี๋ยว")

    def test_update_about(self):
        """ทดสอบการแก้ไขรายละเอียดเมนู"""
        response = self.client.post(reverse("restaurant:edit_only_menu"), {
            "menu_id": self.menu.id,
            "about": "Updated About",
        })
        self.menu.refresh_from_db()
        self.assertEqual(self.menu.about, "Updated About")

    def test_update_price(self):
        """ทดสอบการแก้ไขราคาเมนู"""
        response = self.client.post(reverse("restaurant:edit_only_menu"), {
            "menu_id": self.menu.id,
            "price": "200.00",
        })
        self.menu.refresh_from_db()
        self.assertEqual(self.menu.price, 200.00)

    def test_update_menu_picture(self):
        """ทดสอบการอัปโหลดรูปภาพเมนู"""
        with open("test_image.jpg", "wb") as f:
            f.write(b"Test image content")

        with open("test_image.jpg", "rb") as image_file:
            response = self.client.post(
                reverse("restaurant:edit_only_menu"),
                {"menu_id": self.menu.id, "menu_picture": image_file},
            )
    
        self.assertEqual(response.status_code, 200)
    
        # Refresh the menu object to get the updated picture
        self.menu.refresh_from_db()

        # Check if the file name starts with the original file name
        uploaded_file_name = self.menu.menu_picture.name.split("/")[-1]
        self.assertTrue(uploaded_file_name.startswith("test_image"))
        self.assertTrue(uploaded_file_name.endswith(".jpg"))

    def test_delete_menu(self):
        """ทดสอบการลบเมนู"""
        response = self.client.post(reverse("restaurant:edit_only_menu"), {
            "menu_id": self.menu.id,
            "delete_menu": "true",
        })
        self.assertRedirects(response, reverse("restaurant:edit_menu_payment"))
        with self.assertRaises(Menu.DoesNotExist):
            Menu.objects.get(id=self.menu.id)

    def test_missing_menu_id(self):
        """ทดสอบการส่งคำขอโดยไม่มี menu_id"""
        response = self.client.post(reverse("restaurant:edit_only_menu"))
        self.assertEqual(response.status_code, 404)

    def test_invalid_menu_id(self):
        """ทดสอบการส่งคำขอด้วย menu_id ที่ไม่มีในระบบ"""
        response = self.client.post(reverse("restaurant:edit_only_menu"), {
            "menu_id": 999,
        })
        self.assertEqual(response.status_code, 404)

class EditOnlyPaymentTestCase(TestCase):
    def setUp(self):
     
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            user_type="restaurant"
        )
 
        self.restaurant_profile = RestaurantProfile.objects.create(
            user_profile=self.user_profile,
            restaurant_name="Test Restaurant"
        )

        self.payment_method = PaymentMethod.objects.create(
            bank_name="Test Bank",
            account_number="123456789",
            restaurant_profile=self.restaurant_profile
        )

        # Login ด้วย Client
        self.client = Client()
        self.client.login(username="testuser", password="password123")
        
    def test_get_request_without_payment_id(self):
        response = self.client.get(reverse("restaurant:edit_only_payment"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("restaurant", response.context)
        self.assertIsNone(response.context["payment_item"])

    def test_get_request_with_payment_id(self):
        response = self.client.get(reverse("restaurant:edit_only_payment"), {"payment_id": self.payment_method.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["payment_item"], self.payment_method)

    def test_post_request_to_update_bank_name(self):
        response = self.client.post(reverse("restaurant:edit_only_payment"), {
            "payment_id": self.payment_method.id,
            "bank_name": "Updated Bank"
        })
        self.assertEqual(response.status_code, 200)
        self.payment_method.refresh_from_db()
        self.assertEqual(self.payment_method.bank_name, "Updated Bank")

    def test_post_request_to_update_account_number(self):
        response = self.client.post(reverse("restaurant:edit_only_payment"), {
            "payment_id": self.payment_method.id,
            "account_number": "987654321"
        })
        self.assertEqual(response.status_code, 200)
        self.payment_method.refresh_from_db()
        self.assertEqual(self.payment_method.account_number, "987654321")

    def test_post_request_to_delete_payment_method(self):
        response = self.client.post(reverse("restaurant:edit_only_payment"), {
            "payment_id": self.payment_method.id,
            "delete_payment_method": "true"
        })
        self.assertRedirects(response, reverse("restaurant:edit_menu_payment"))
        with self.assertRaises(PaymentMethod.DoesNotExist):
            PaymentMethod.objects.get(id=self.payment_method.id)

    def test_post_request_with_invalid_payment_id(self):
        response = self.client.post(reverse("restaurant:edit_only_payment"), {
            "payment_id": 9999,  # Non-existent ID
        })
        self.assertEqual(response.status_code, 404)

    def test_get_request_with_invalid_payment_id(self):
        response = self.client.get(reverse("restaurant:edit_only_payment"), {"payment_id": 9999})
        self.assertEqual(response.status_code, 404)

from pytz import timezone
from datetime import datetime
from django.utils.timezone import make_aware
class SalesReportTestCase(TestCase):
    def setUp(self):
        local_tz = timezone("Asia/Bangkok")   

        self.user = User.objects.create_user(username="testuser", password="password123")
        self.user_profile = UserProfile.objects.create(user=self.user, user_type="restaurant")
        self.restaurant = RestaurantProfile.objects.create(
            user_profile=self.user_profile,
            restaurant_name="Test Restaurant"
        )

        self.order1 = Order.objects.create(
            user_profile=self.user_profile,
            restaurant=self.restaurant,
            total_price=100.00,
            order_date=make_aware(datetime(2024, 12, 10, 10, 0, 0), local_tz),
            status='completed'
        )
        self.order2 = Order.objects.create(
            user_profile=self.user_profile,
            restaurant=self.restaurant,
            total_price=200.00,
            order_date=make_aware(datetime(2024, 12, 12, 14, 0, 0), local_tz),
            status='completed'
        )
        self.order3 = Order.objects.create(
            user_profile=self.user_profile,
            restaurant=self.restaurant,
            total_price=50.00,
            order_date=make_aware(datetime(2024, 12, 8, 0, 0, 0), local_tz),
            status='completed'
        )

        self.client = Client()
        self.client.login(username="testuser", password="password123")
        
    def test_sales_report(self):
        response = self.client.get(reverse("restaurant:sales_report"))
        
    def test_sales_report_without_date_filter(self):
        response = self.client.get(reverse("restaurant:sales_report"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["total_sales"], 350.00)  # Total of completed orders
        self.assertEqual(len(response.context["orders"]), 3)  # Completed orders only
        self.assertEqual(response.context["restaurant"], self.restaurant)

    def test_sales_report_no_completed_orders(self):
        # Set all orders to a non-completed status
        Order.objects.filter(status='completed').update(status='cooking')
        response = self.client.get(reverse("restaurant:sales_report"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["total_sales"], 0)  # No completed orders
        self.assertEqual(len(response.context["orders"]), 0)  # No orders in context

class AddPaymentTestCase(TestCase):
    def setUp(self):
        # สร้าง user และ restaurant profile
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.user_profile = UserProfile.objects.create(user=self.user, user_type="restaurant")
        self.restaurant_profile = RestaurantProfile.objects.create(
            user_profile=self.user_profile,
            restaurant_name="Test Restaurant"
        )

        self.client = Client()

    def test_add_payment_success(self):
        """ทดสอบการเพิ่มบัญชีธนาคารเมื่อข้อมูลถูกต้อง"""
        self.client.login(username="testuser", password="password123")

        response = self.client.post(reverse('restaurant:add_payment'), {
            'bank_name': 'Test Bank',
            'account_number': '1234567890',
        })

        # ตรวจสอบการสร้างข้อมูล PaymentMethod
        self.assertTrue(PaymentMethod.objects.filter(bank_name='Test Bank', account_number='1234567890').exists())

        # ตรวจสอบ redirect
        self.assertRedirects(response, reverse('restaurant:edit_menu_payment'))

    def test_add_payment_missing_fields(self):
        """ทดสอบการเพิ่มบัญชีธนาคารเมื่อข้อมูลไม่ครบถ้วน"""
        self.client.login(username="testuser", password="password123")

        response = self.client.post(reverse('restaurant:add_payment'), {
            'bank_name': '',  # ไม่ใส่ชื่อธนาคาร
            'account_number': '',
        })

        # ตรวจสอบว่าไม่มีการสร้าง PaymentMethod
        self.assertFalse(PaymentMethod.objects.exists())

        # ตรวจสอบ error message
        self.assertContains(response, "กรุณากรอกชื่อธนาคารและเลขบัญชีให้ครบถ้วน")

    def test_add_payment_get_request(self):
        """ทดสอบการแสดงรายการบัญชีธนาคารเมื่อใช้ GET"""
        self.client.login(username="testuser", password="password123")

        # เพิ่มข้อมูล PaymentMethod ล่วงหน้า
        PaymentMethod.objects.create(
            restaurant_profile=self.restaurant_profile,
            bank_name="Test Bank 1",
            account_number="1234567890"
        )

        response = self.client.get(reverse('restaurant:add_payment'))

        # ตรวจสอบการแสดงผล
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Bank 1")
        self.assertContains(response, "1234567890")

    def test_add_payment_duplicate_entry(self):
        """ทดสอบการเพิ่มบัญชีธนาคารซ้ำกัน"""
        self.client.login(username="testuser", password="password123")

        # เพิ่มบัญชีธนาคารครั้งแรก
        PaymentMethod.objects.create(
            restaurant_profile=self.restaurant_profile,
            bank_name="Test Bank",
            account_number="1234567890"
        )

        # ส่งข้อมูลซ้ำ
        response = self.client.post(reverse('restaurant:add_payment'), {
            'bank_name': 'Test Bank',
            'account_number': '1234567890',
        })

        # ตรวจสอบว่าไม่มีการสร้างบัญชีซ้ำ
        self.assertEqual(PaymentMethod.objects.filter(
            bank_name='Test Bank',
            account_number='1234567890'
        ).count(), 1)

        # ตรวจสอบ error message (เพิ่ม validation ใน view ถ้าจำเป็น)
        self.assertContains(response, "บัญชีนี้มีอยู่แล้ว")
    
    def test_add_payment_invalid_account_number(self):
        """ทดสอบการเพิ่มบัญชีธนาคารที่เลขบัญชีไม่ใช่ตัวเลข"""
        self.client.login(username="testuser", password="password123")

        response = self.client.post(reverse('restaurant:add_payment'), {
            'bank_name': 'Test Bank',
            'account_number': 'invalid123',
        })

        # ตรวจสอบว่าไม่มีการสร้าง PaymentMethod
        self.assertFalse(PaymentMethod.objects.exists())

        # ตรวจสอบ error message
        self.assertContains(response, "กรุณากรอกเลขบัญชีที่ถูกต้อง")
    def test_add_payment_only_show_user_methods(self):
        """ทดสอบว่าแสดงเฉพาะบัญชีธนาคารของผู้ใช้งานปัจจุบัน"""
        other_user = User.objects.create_user(username="otheruser", password="password456")
        other_user_profile = UserProfile.objects.create(user=other_user, user_type="restaurant")
        other_restaurant_profile = RestaurantProfile.objects.create(
            user_profile=other_user_profile,
            restaurant_name="Other Restaurant"
        )

        # เพิ่มบัญชีธนาคารของผู้ใช้อื่น
        PaymentMethod.objects.create(
            restaurant_profile=other_restaurant_profile,
            bank_name="Other Bank",
            account_number="999999999"
        )

        # เพิ่มบัญชีธนาคารของผู้ใช้ปัจจุบัน
        PaymentMethod.objects.create(
            restaurant_profile=self.restaurant_profile,
            bank_name="My Bank",
            account_number="1234567890"
        )

        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse('restaurant:add_payment'))

        # ตรวจสอบการแสดงผล
        self.assertContains(response, "My Bank")
        self.assertContains(response, "1234567890")
        self.assertNotContains(response, "Other Bank")
