from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import UserProfile, RestaurantProfile, Menu,Order,OrderItem,PaymentMethod
from restaurant import *
from django.contrib.messages import get_messages
from django.shortcuts import get_object_or_404

class ViewsTestsCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="somtamkaiyang", password="Pass@somtam2")
        self.profile = UserProfile.objects.create(user=self.user, name="Yingthai Jaingam", phone_number=66912345678, email="yingthaijai@gmail.com", user_type="restaurant")
        self.restaurant = RestaurantProfile.objects.create(restaurant_name="Somtam YingThai", food_category="อาหารตามสั่ง", about="ขายส้มตำ ไก่ย่าง แซ่บๆ")
        self.menu = Menu.objects.create(food_name="ส้มตำไทย",food_category="ส้มตำ", about="ส้มตำไทย อร่อย ถูกใจวัยรุ่น" )
        self.url = reverse('choose_regis')

    def test_index_page(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
    
    def test_kinkorn_navigator(self):
        response = self.client.get(reverse("kinkorn"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

    def test_about_navigator(self):
        response = self.client.get(reverse("about"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "about.html")

    def test_order_navigator(self):
        response = self.client.get(reverse("order"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

    def test_yourorder_navigator(self):
        response = self.client.get(reverse("yourorder"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

    def test_choose_register_page(self):
        response = self.client.post(reverse("choose_regis"), {"user_type": "restaurant"})
        session = self.client.session
        self.assertEqual(session["user_type"], "restaurant")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/register/")

    def test_register_page(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "register.html")

    def test_successful_user_registration(self):
        response = self.client.post(reverse("register"), {
            "username": "sushinumberome",
            "password": "Pass@sushi1",
            "confirmpassword": "Pass@sushi1",
            "phone_number": "66987654321",
            "name": "sushi",
            "email": "sushinumberone@gmail.com",
            "user_type": "restaurant",
            "profile_picture": "",
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="sushinumberome").exists())
        self.assertTrue(UserProfile.objects.filter(user__username="sushinumberome").exists())

    def test_login_page(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")

    def test_successful_login(self):
        response = self.client.post(reverse("login"), {
            "username": "somtamkaiyang",
            "password": "Pass@somtam2"
        })
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Login successfully!")

    def test_restaurant_register_page(self):
        self.client.login(username="somtamkaiyang", password="Pass@somtam2")
        response = self.client.get(reverse("restaurant_register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "restaurant_register.html")

    def test_add_menu_success(self):
        self.client.login(username="somtamkaiyang", password="Pass@somtam2")
        response = self.client.post(
            reverse("add_menu") + "?restaurant_name=Somtam YingThai", 
            {
                "food_name": "ส้มตำปูปลาร้า",
                "food_category": "อาหารตามสั่ง",
                "about": "ส้มตำปูปลาร้า อร่อย ถูกใจวัยรุ่น",
                "price": "50",
                "menu_picture": "",
                "restaurant_name": "Somtam YingThai",
                "user_type": "restaurant"
            }
        )
        expected_url = reverse("welcome_registration") + "?user_type=restaurant&restaurant_name=Somtam%20YingThai"
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url)
        self.assertTrue(Menu.objects.filter(food_name="ส้มตำปูปลาร้า").exists())

    def test_post_request_restaurant_redirect(self):
        response = self.client.post(self.url, {'user_type': 'restaurant'})
        self.assertRedirects(response, reverse('register'))


    def test_get_request_renders_template(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'choose_regis.html')

class LoginViewTest(TestCase):
    def setUp(self):
        # สร้างผู้ใช้ประเภท restaurant
        self.restaurant_user = User.objects.create_user(username="restaurant_user", password="testpassword")
        UserProfile.objects.create(user=self.restaurant_user, user_type="restaurant")  # กำหนด user_type เป็น restaurant
        self.url = reverse("login")

        # สร้างผู้ใช้ประเภท customer
        self.customer_user = User.objects.create_user(username="customer_user", password="testpassword")
        self.customer_profile = UserProfile.objects.create(user=self.customer_user, user_type="customer")

        # Client สำหรับทดสอบ
        self.client = Client()
        self.url = reverse("login")  # URL สำหรับ login view


    def test_login_success_as_customer(self):
        """ทดสอบการล็อกอินสำเร็จสำหรับผู้ใช้ประเภท customer"""
        response = self.client.post(self.url, {"username": "customer_user", "password": "testpassword"})
        self.assertRedirects(response, "/order/")
        messages = list(response.wsgi_request._messages)
        self.assertEqual(str(messages[0]), "Login successfully!")

    def test_login_failure_invalid_credentials(self):
        """ทดสอบการล็อกอินล้มเหลวเมื่อใช้ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง"""
        response = self.client.post(self.url, {"username": "wronguser", "password": "wrongpassword"})
        self.assertTemplateUsed(response, "login.html")
        messages = list(response.wsgi_request._messages)
        self.assertEqual(str(messages[0]), "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")
 

        
from django.utils import timezone
from django.utils.timezone import make_aware
class YourOrderViewTest(TestCase):
    def setUp(self):
        # Set up test client and data
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.user_profile = UserProfile.objects.create(user=self.user, user_type='customer')
        
       
        self.restaurant_profile = RestaurantProfile.objects.create(
            user_profile=self.user_profile,
            restaurant_name="Test Restaurant",
            about="A test restaurant",
            open_close_time="9:00 AM - 9:00 PM",
            food_category="MADE_TO_ORDER"
        )


        self.order = Order.objects.create(
            user_profile=self.user_profile,
            restaurant=self.restaurant_profile,  # Include restaurant profile here
            status='waiting_for_payment',
            total_price=100.0
        )
        
        self.menu = Menu.objects.create(
        restaurant_profile=self.restaurant_profile,
        food_name="Test Menu",
        price=50.0
        )
        
    def test_save_order_not_found(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(reverse('your_order'), {
            'save_order': True,
            'order_id': 9999,  # Invalid order ID
            'pickup_time': '2024-12-12T10:00',
            'delivery_option': 'in_store'
        })
        messages = list(response.wsgi_request._messages)
        self.assertIn("ไม่พบคำสั่งซื้อที่ต้องการบันทึก", [msg.message for msg in messages])

    def test_delete_item_not_found(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse('your_order'),
            {
                'delete_item': True,
                'item_id': 9999,  # Invalid item_id
            }
        )
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "ไม่พบรายการที่ต้องการลบ")

    def test_add_menu_not_found(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse('your_order'),
            {
                'menu_id': 9999,  # Invalid menu_id
            }
        )
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "เมนูที่เลือกไม่มีอยู่ในระบบ")
    
    def test_save_order_success(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse('your_order'),
            {
                'save_order': True,
                'order_id': self.order.id,
                'pickup_time': '2024-12-12T10:00',
                'delivery_option': 'in_store'
            }
        )
        self.order.refresh_from_db()
        self.assertEqual(response.status_code, 302)

        # แปลงค่า expected datetime เป็น Time Zone-aware
        expected_pickup_time = make_aware(timezone.datetime(2024, 12, 12, 10, 0))
        self.assertEqual(self.order.pickup_time, expected_pickup_time)
        self.assertEqual(self.order.delivery_option, 'in_store')
        
        
    def test_add_menu_new_item(self):
        menu = Menu.objects.create(
            restaurant_profile=self.restaurant_profile,
            food_name="New Menu",
            price=100.0
        )
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse('your_order'),
            {
                'menu_id': menu.id
            }
        )
        self.assertEqual(response.status_code, 302)
        order = Order.objects.get(id=self.order.id)
        self.assertEqual(order.order_items.count(), 1)
        
    def test_add_menu_update_quantity(self):
        menu = Menu.objects.create(
            restaurant_profile=self.restaurant_profile,
            food_name="Test Menu",
            price=50.0
        )
        order_item = OrderItem.objects.create(
            order=self.order,
            restaurant_menu=menu,
            quantity=1,
            total_price=50.0
        )
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse('your_order'),
            {
                'menu_id': menu.id
            }
        )
        self.assertEqual(response.status_code, 302)
        order_item.refresh_from_db()
        self.assertEqual(order_item.quantity, 2)
        self.assertEqual(order_item.total_price, 100.0)
        
    def test_get_orders(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse('your_order'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Restaurant")
        self.assertContains(response, "100.0")

    def test_delete_item_success(self):
        menu = Menu.objects.create(restaurant_profile=self.restaurant_profile, food_name="Test Menu", price=50.0)
        order_item = OrderItem.objects.create(order=self.order, restaurant_menu=menu, quantity=1, total_price=50.0)

        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(reverse('your_order'), {'delete_item': True, 'item_id': order_item.id})

        with self.assertRaises(OrderItem.DoesNotExist):
            OrderItem.objects.get(id=order_item.id)
            
    def test_delete_item_order_deleted(self):
        menu = Menu.objects.create(
            restaurant_profile=self.restaurant_profile,
            food_name="Single Menu",
            price=50.0
        )
        order_item = OrderItem.objects.create(
            order=self.order,
            restaurant_menu=menu,
            quantity=1,
            total_price=50.0
        )

        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse('your_order'),
            {'delete_item': True, 'item_id': order_item.id}
        )

   
        with self.assertRaises(Order.DoesNotExist):
            Order.objects.get(id=self.order.id)

       
        self.assertEqual(response.status_code, 302)


    def test_delete_item_order_total_price_updated(self):
    
        menu1 = Menu.objects.create(
            restaurant_profile=self.restaurant_profile,
            food_name="Menu 1",
            price=50.0
        )
        menu2 = Menu.objects.create(
            restaurant_profile=self.restaurant_profile,
            food_name="Menu 2",
            price=30.0
        )
        order_item1 = OrderItem.objects.create(
            order=self.order,
            restaurant_menu=menu1,
            quantity=1,
            total_price=50.0
        )
        order_item2 = OrderItem.objects.create(
            order=self.order,
            restaurant_menu=menu2,
            quantity=1,
            total_price=30.0
        )


        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse('your_order'),
            {'delete_item': True, 'item_id': order_item1.id}
        )

        self.order.refresh_from_db()
        self.assertEqual(self.order.order_items.count(), 1)

        self.assertEqual(self.order.total_price, 30.0)

  
        self.assertEqual(response.status_code, 302)
        

    
    


from django.core.files.uploadedfile import SimpleUploadedFile
class UploadPaymentSlipTest(TestCase):
    def setUp(self):
        # Set up test client and data
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.user_profile = UserProfile.objects.create(user=self.user, user_type='customer')

        # Create a test restaurant profile
        self.restaurant_profile = RestaurantProfile.objects.create(
            user_profile=self.user_profile,
            restaurant_name="Test Restaurant",
            about="A test restaurant",
            open_close_time="9:00 AM - 9:00 PM",
            food_category=RestaurantProfile.Foodcate.MADE_TO_ORDER
        )

        # Create a test payment method for the restaurant
        self.payment_method = PaymentMethod.objects.create(
            restaurant_profile=self.restaurant_profile,
            bank_name="Test Bank",
            account_number="1234567890"
        )

        # Create a test order
        self.order = Order.objects.create(
            user_profile=self.user_profile,
            restaurant=self.restaurant_profile,
            status='waiting_for_payment',
            total_price=100.0
        )

    def test_upload_payment_slip_success(self):
        self.client.login(username="testuser", password="testpassword")
        
        # Create a fake payment slip file
        payment_slip = SimpleUploadedFile(
            "slip.jpg", 
            b"fake-image-content", 
            content_type="image/jpeg"
        )
        
        # Perform POST request with the payment slip
        response = self.client.post(
            reverse('upload_payment_slip', args=[self.order.id]),
            {'payment_slip': payment_slip}
        )
        
        # Refresh the order object from the database
        self.order.refresh_from_db()

        # Assert the order status is updated and payment slip is saved
        self.assertEqual(response.status_code, 302)  # Redirect status
        self.assertEqual(self.order.status, 'waiting_for_approve')
        self.assertTrue(self.order.payment_slip)  # Ensure payment slip is set

    def test_upload_payment_slip_no_file(self):
        self.client.login(username="testuser", password="testpassword")

        # Perform POST request without a payment slip
        response = self.client.post(reverse('upload_payment_slip', args=[self.order.id]))

        # Refresh the order object from the database
        self.order.refresh_from_db()

        # Assert the order status is not updated
        self.assertEqual(response.status_code, 302)  # Redirect status
        self.assertEqual(self.order.status, 'waiting_for_payment')
        self.assertFalse(self.order.payment_slip)  # Ensure no file is uploaded
        
class OrderConfirmationTest(TestCase):
    def setUp(self):
        # Set up test client and data
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.user_profile = UserProfile.objects.create(user=self.user, user_type='customer')

        # Create a test restaurant profile
        self.restaurant_profile = RestaurantProfile.objects.create(
            user_profile=self.user_profile,
            restaurant_name="Test Restaurant",
            about="A test restaurant",
            open_close_time="9:00 AM - 9:00 PM",
            food_category=RestaurantProfile.Foodcate.MADE_TO_ORDER
        )

        # Create a test payment method for the restaurant
        self.payment_method = PaymentMethod.objects.create(
            restaurant_profile=self.restaurant_profile,
            bank_name="Test Bank",
            account_number="1234567890"
        )

        # Create an order with items
        self.order_with_items = Order.objects.create(
            user_profile=self.user_profile,
            restaurant=self.restaurant_profile,
            status='waiting_for_payment',
            total_price=100.0
        )

        self.menu_item = Menu.objects.create(
            restaurant_profile=self.restaurant_profile,
            food_name="Test Menu Item",
            about="Test Description",
            price=50.0
        )

        self.order_item = OrderItem.objects.create(
            order=self.order_with_items,
            restaurant_menu=self.menu_item,
            quantity=2,
            total_price=100.0
        )


        self.empty_order = Order.objects.create(
            user_profile=self.user_profile,
            restaurant=self.restaurant_profile,
            status='waiting_for_payment',
            total_price=0.0
        )

    def test_confirm_order_with_items(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(reverse('order_confirmation'), {'order_id': self.order_with_items.id})
        self.order_with_items.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.order_with_items.status, 'paid')
        messages = list(get_messages(response.wsgi_request))
        self.assertIn("ยืนยันคำสั่งซื้อเรียบร้อยแล้ว!", [message.message for message in messages])
    

class RestaurantRegisterViewTest(TestCase):
    def setUp(self):
        # สร้างผู้ใช้
        self.client = Client()
        self.user = User.objects.create_user(username="somtamkaiyang", password="Pass@somtam2")
        self.profile = UserProfile.objects.create(
            user=self.user,
            name="Yingthai Jaingam",
            phone_number=66912345678,
            email="yingthaijai@gmail.com",
            user_type="restaurant"
        )
        self.url = reverse("restaurant_register")  # URL ของฟังก์ชัน restaurant_register

        # ล็อกอิน
        self.client.login(username="somtamkaiyang", password="Pass@somtam2")

    def test_get_request_renders_template(self):
        response = self.client.get(self.url)

        # ตรวจสอบว่า response status เป็น 200
        self.assertEqual(response.status_code, 200)

        # ตรวจสอบว่า template ถูก render
        self.assertTemplateUsed(response, "restaurant_register.html")

        # ตรวจสอบ context
        self.assertEqual(response.context["username"], "somtamkaiyang")
        self.assertIn("food_categories", response.context)
        
    def test_post_request_creates_restaurant_with_picture(self):
        # อัปโหลดไฟล์รูปภาพจำลอง
        image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")

        # ส่งข้อมูล POST
        response = self.client.post(self.url, {
            "restaurant_name": "Somtam YingThai",
            "food_category": "อาหารตามสั่ง",
            "about": "ขายส้มตำ ไก่ย่าง แซ่บๆ",
            "open_close_time": "9:00 AM - 8:00 PM",
            "restaurant_picture": image,
        })

        # ตรวจสอบว่า redirect ไปยัง add_menu
        self.assertRedirects(response, reverse("add_menu") + "?restaurant_name=Somtam YingThai")

        # ตรวจสอบว่าข้อมูลถูกบันทึกในฐานข้อมูล
        restaurant = RestaurantProfile.objects.get(restaurant_name="Somtam YingThai")
        self.assertEqual(restaurant.food_category, "อาหารตามสั่ง")
        self.assertEqual(restaurant.about, "ขายส้มตำ ไก่ย่าง แซ่บๆ")
        self.assertIsNotNone(restaurant.restaurant_picture)
    def test_register_restaurant_without_picture(self):
        """ทดสอบการลงทะเบียนร้านอาหารโดยไม่อัปโหลดรูปภาพ"""
        data = {
            "restaurant_name": "No Image Restaurant",
            "food_category": "อาหารตามสั่ง",
            "about": "A test restaurant without a picture",
            "open_close_time": "9:00 AM - 9:00 PM",
        }

        # ส่ง POST request โดยไม่ใส่ไฟล์รูปภาพ
        response = self.client.post(self.url, data)

        # ตรวจสอบการ redirect ไปยัง add_menu
        self.assertRedirects(response, reverse("add_menu") + "?restaurant_name=No Image Restaurant")

        # ตรวจสอบว่า RestaurantProfile ถูกสร้างขึ้น
        restaurant = RestaurantProfile.objects.get(restaurant_name="No Image Restaurant")
        self.assertEqual(restaurant.food_category, "อาหารตามสั่ง")
        self.assertEqual(restaurant.about, "A test restaurant without a picture")
        self.assertEqual(restaurant.open_close_time, "9:00 AM - 9:00 PM")
        self.assertFalse(restaurant.restaurant_picture)


class RegisterViewTest(TestCase):
    def setUp(self):
        # สร้างผู้ใช้ที่มีอยู่ในระบบแล้ว
        self.client = Client()
        self.user = User.objects.create_user(username="somtamkaiyang", password="Pass@somtam2")
        self.profile = UserProfile.objects.create(
            user=self.user,
            name="Yingthai Jaingam",
            phone_number="66912345678",
            email="yingthaijai@gmail.com",
            user_type="restaurant"
        )
        self.url = reverse("register")  # URL สำหรับฟังก์ชัน register

    def test_get_request_renders_template(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "register.html")
        self.assertEqual(response.context["user_type"], "customer")

    def test_post_request_register_success_customer(self):
        response = self.client.post(self.url, {
            "username": "testcustomer",
            "password": "password123",
            "confirmpassword": "password123",
            "phone_number": "66987654321",
            "email": "customer@test.com",
            "name": "Customer Test",
            "user_type": "customer"
        })

        # ตรวจสอบว่ามีการสร้าง User และ UserProfile
        user = User.objects.get(username="testcustomer")
        profile = UserProfile.objects.get(user=user)
        self.assertEqual(profile.user_type, "customer")

        # ตรวจสอบ redirect ไปยัง welcome_registration
        self.assertRedirects(response, reverse("welcome_registration") + "?user_type=customer&username=testcustomer")

    def test_post_request_register_success_restaurant(self):
        response = self.client.post(self.url, {
            "username": "testrestaurant",
            "password": "password123",
            "confirmpassword": "password123",
            "phone_number": "66987654322",
            "email": "restaurant@test.com",
            "name": "Restaurant Test",
            "user_type": "restaurant"
        })

        # ตรวจสอบว่ามีการสร้าง User และ UserProfile
        user = User.objects.get(username="testrestaurant")
        profile = UserProfile.objects.get(user=user)
        self.assertEqual(profile.user_type, "restaurant")

        # ตรวจสอบ redirect ไปยัง restaurant_register
        self.assertRedirects(response, reverse("restaurant_register"))

    def test_post_request_username_already_exists(self):
        response = self.client.post(self.url, {
            "username": "somtamkaiyang",  # ซ้ำกับผู้ใช้ที่มีอยู่แล้ว
            "password": "password123",
            "confirmpassword": "password123",
            "phone_number": "66987654321",
            "email": "newemail@test.com",
            "name": "Test User",
            "user_type": "customer"
        })

        self.assertContains(response, "This username is already used.")
        self.assertEqual(response.status_code, 200)

    def test_post_request_email_already_exists(self):
        response = self.client.post(self.url, {
            "username": "newuser",
            "password": "password123",
            "confirmpassword": "password123",
            "phone_number": "66987654321",
            "email": "yingthaijai@gmail.com",  # ซ้ำกับ email ที่มีอยู่แล้ว
            "name": "Test User",
            "user_type": "customer"
        })

        self.assertContains(response, "This email is already used.")
        self.assertEqual(response.status_code, 200)

    def test_post_request_password_mismatch(self):
        response = self.client.post(self.url, {
            "username": "newuser",
            "password": "password123",
            "confirmpassword": "password321",  # รหัสผ่านไม่ตรงกัน
            "phone_number": "66987654321",
            "email": "newemail@test.com",
            "name": "Test User",
            "user_type": "customer"
        })

        self.assertContains(response, "Password do not match.")
        self.assertEqual(response.status_code, 200)
    def test_register_with_profile_picture(self):
        image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")

        response = self.client.post(self.url, {
            "username": "user_with_image",
            "password": "password123",
            "confirmpassword": "password123",
            "phone_number": "66911223344",
            "email": "user_with_image@test.com",
            "name": "User Image Test",
            "user_type": "customer",
            "profile_picture": image
        })

        # ตรวจสอบการ redirect
        self.assertRedirects(response, reverse("welcome_registration") + "?user_type=customer&username=user_with_image")

        # ตรวจสอบว่า User และ UserProfile ถูกสร้าง
        user = User.objects.get(username="user_with_image")
        profile = UserProfile.objects.get(user=user)
        self.assertIsNotNone(profile.profile_picture)
    
    def test_register_with_no_user_type(self):
        response = self.client.post(self.url, {
            "username": "no_usertype_user",
            "password": "password123",
            "confirmpassword": "password123",
            "phone_number": "66912345679",
            "email": "no_usertype@test.com",
            "name": "No UserType"
        })

        user = User.objects.get(username="no_usertype_user")
        profile = UserProfile.objects.get(user=user)

        self.assertEqual(profile.user_type, "customer")
        self.assertRedirects(response, reverse("welcome_registration") + "?user_type=customer&username=no_usertype_user")

    def test_post_request_phone_number_already_exists(self):
        response = self.client.post(self.url, {
            "username": "newuser2",
            "password": "password123",
            "confirmpassword": "password123",
            "phone_number": "66912345678",  # เบอร์ที่ซ้ำกับในฐานข้อมูล
            "email": "newuser2@test.com",
            "name": "Test User2",
            "user_type": "customer"
        })

        self.assertContains(response, "This phone number is already used.")
        self.assertEqual(response.status_code, 200)

        
from django.contrib.auth.hashers import make_password
from home.views import authenticate_user_profile
class AuthenticateUserProfileTest(TestCase):
    def setUp(self):
        # สร้างข้อมูลผู้ใช้งาน
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            name="Test User",
            email="testuser@example.com",
            phone_number="66912345678",
            user_type="customer"
        )
        # เข้ารหัสรหัสผ่าน
        self.user_profile.password = make_password("testpassword")
        self.user_profile.save()

    def test_authenticate_success(self):
        """ทดสอบเข้าสู่ระบบสำเร็จ"""
        user = authenticate_user_profile(username="testuser", password="testpassword")
        self.assertIsNotNone(user)
        self.assertEqual(user, self.user_profile)

    def test_authenticate_invalid_username(self):
        """ทดสอบเมื่อชื่อผู้ใช้ไม่ถูกต้อง"""
        user = authenticate_user_profile(username="invaliduser", password="testpassword")
        self.assertIsNone(user)

    def test_authenticate_invalid_password(self):
        """ทดสอบเมื่อรหัสผ่านไม่ถูกต้อง"""
        user = authenticate_user_profile(username="testuser", password="wrongpassword")
        self.assertIsNone(user)

    def test_authenticate_no_user_profiles(self):
        """ทดสอบเมื่อไม่มีข้อมูลผู้ใช้งาน"""
        UserProfile.objects.all().delete()
        user = authenticate_user_profile(username="testuser", password="testpassword")
        self.assertIsNone(user) 
   
        
from django.contrib.auth import get_user
class LogoutViewTest(TestCase):
    def setUp(self):
        # สร้างผู้ใช้
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.login(username="testuser", password="testpassword")  
        self.url = reverse("logout")  

    def test_logout_successful(self):
        response = self.client.get(self.url)
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)  

       
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Logout successfully!")

    
        self.assertRedirects(response, '/')
        
class RestaurantListViewTest(TestCase):
    def setUp(self):
     
        self.client = Client()
        self.user1 = User.objects.create_user(username="user1", password="password123")
        self.profile1 = UserProfile.objects.create(user=self.user1, user_type="restaurant")

        self.user2 = User.objects.create_user(username="user2", password="password123")
        self.profile2 = UserProfile.objects.create(user=self.user2, user_type="restaurant")

     
        self.restaurant1 = RestaurantProfile.objects.create(
            user_profile=self.profile1,
            restaurant_name="Restaurant 1",
            food_category="MADE_TO_ORDER",
            about="A test restaurant",
            open_close_time="9:00 AM - 9:00 PM"
        )
        self.restaurant2 = RestaurantProfile.objects.create(
            user_profile=self.profile2,
            restaurant_name="Restaurant 2",
            food_category="RICE_AND_CURRY",
            about="Another test restaurant",
            open_close_time="10:00 AM - 8:00 PM"
        )

        self.url = reverse('restaurant_list')  

    def test_restaurant_list_view(self):
      
        response = self.client.get(self.url)

 
        self.assertEqual(response.status_code, 200)

 
        self.assertTemplateUsed(response, 'order.html')

   
        restaurants = response.context['restaurants']
        self.assertEqual(restaurants.count(), 2)
        self.assertIn(self.restaurant1, restaurants)
        self.assertIn(self.restaurant2, restaurants)

   
from datetime import datetime, timedelta
from django.utils.timezone import make_aware, now

        
class OrderStatusViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        user_profile = UserProfile.objects.create(user=self.user, user_type='customer')

        self.restaurant_profile = RestaurantProfile.objects.create(
            user_profile=user_profile,
            restaurant_name="Test Restaurant"
        )

        self.order_today = Order.objects.create(
            user_profile=user_profile,
            restaurant=self.restaurant_profile,
            order_date=timezone.make_aware(datetime(2024, 12, 10, 12, 0)),
            total_price=100,
            status="completed"
        )

        self.order_yesterday = Order.objects.create(
            user_profile=user_profile,
            restaurant=self.restaurant_profile,
            order_date=timezone.make_aware(datetime(2024, 12, 9, 12, 0)),
            total_price=150,
            status="completed"
        )

        self.order_older = Order.objects.create(
            user_profile=user_profile,
            restaurant=self.restaurant_profile,
            order_date=timezone.make_aware(datetime(2024, 12, 8, 12, 0)),
            total_price=200,
            status="completed"
        )

        self.client.login(username="testuser", password="password")
        self.url = reverse("order_status")

    def test_order_status_default_date(self):
        # อัปเดตเวลาหลังจากสร้าง order เพื่อให้เวลาตรงตามเงื่อนไข
        self.order_today.order_date = timezone.make_aware(datetime.now())
        self.order_today.save()

        self.order_yesterday.order_date = timezone.make_aware(datetime.now() - timedelta(days=1))
        self.order_yesterday.save()

        self.order_older.order_date = timezone.make_aware(datetime.now() - timedelta(days=7))
        self.order_older.save()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        orders = response.context['orders']

        # ตรวจสอบว่าเฉพาะ order_today ถูกกรอง
        self.assertIn(self.order_today, orders)
        self.assertNotIn(self.order_yesterday, orders)
        self.assertNotIn(self.order_older, orders)
    def test_order_status_invalid_selected_date(self):
        
        """ทดสอบกรณีที่ selected_date ไม่ถูกต้อง"""
        response = self.client.get(self.url, {'selected_date': 'invalid-date'})
        
        # ตรวจสอบว่ามีข้อความ error
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(str(messages_list[0]), "รูปแบบวันที่ไม่ถูกต้อง กรุณาเลือกวันที่อีกครั้ง.")

        # ตรวจสอบว่า selected_date ถูก fallback เป็น today
        self.assertEqual(response.context['selected_date'], datetime.now().date())

class AddMenuViewTest(TestCase):
    def setUp(self):
        # สร้าง Client สำหรับทดสอบ
        self.client = Client()

        # สร้างผู้ใช้และโปรไฟล์ร้านอาหาร
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.user_profile = UserProfile.objects.create(user=self.user, user_type="restaurant")
        self.restaurant_profile = RestaurantProfile.objects.create(
            user_profile=self.user_profile,
            restaurant_name="Test Restaurant",
            food_category="FOOD",
            about="A great restaurant",
            open_close_time="9:00 AM - 8:00 PM"
        )

        # URL สำหรับ add_menu
        self.url = reverse("add_menu") + "?restaurant_name=Test Restaurant"

    def test_get_request_renders_template(self):
        """ทดสอบการแสดงผล Template เมื่อใช้ HTTP GET"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "add_menu.html")
        self.assertEqual(response.context["restaurant_name"], "Test Restaurant")
        self.assertIn("food_categories", response.context)

    def test_post_request_add_menu_with_picture(self):
        """ทดสอบการเพิ่มเมนูพร้อมรูปภาพ"""
        # สร้างไฟล์รูปภาพจำลอง
        image = SimpleUploadedFile("menu_picture.jpg", b"file_content", content_type="image/jpeg")

        response = self.client.post(self.url, {
            "food_name": "Pad Thai",
            "food_category": "Noodles",
            "about": "Delicious Pad Thai",
            "price": 100.0,
            "menu_picture": image,
        })

        # ตรวจสอบ redirect ไปยัง welcome_registration
        self.assertRedirects(response, reverse("welcome_registration") + "?user_type=restaurant&restaurant_name=Test Restaurant")

        # ตรวจสอบข้อมูลในฐานข้อมูล
        menu_item = Menu.objects.get(food_name="Pad Thai")
        self.assertEqual(menu_item.food_category, "Noodles")
        self.assertEqual(menu_item.price, 100.0)
        self.assertIsNotNone(menu_item.menu_picture)
        
class ChooseRegisViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            name="Test User",
            email="testuser@example.com",
            phone_number="66912345678",
            user_type="customer"
        )
        self.user_profile.save()

        self.client = Client()
        self.url = reverse('choose_regis')  # URL สำหรับ choose_regis view

    def test_get_request_renders_template(self):
        """ทดสอบการแสดงผล template สำหรับ GET request"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "choose_regis.html")

    def test_post_request_user_type_restaurant(self):
        """ทดสอบการ redirect ไปที่ register เมื่อเลือก user_type เป็น restaurant"""
        response = self.client.post(self.url, {"user_type": "restaurant"})
        self.assertRedirects(response, reverse("register"))

        # ตรวจสอบว่าค่าใน session ถูกบันทึกถูกต้อง
        session = self.client.session
        self.assertEqual(session["user_type"], "restaurant")

    def test_post_request_user_type_customer(self):
        """ทดสอบการ redirect ไปที่ customer_register เมื่อเลือก user_type เป็น customer"""
        response = self.client.post(self.url, {"user_type": "customer"})
        self.assertRedirects(response, reverse("register"))

        # ตรวจสอบว่าค่าใน session ถูกบันทึกถูกต้อง
        session = self.client.session
        self.assertEqual(session["user_type"], "customer")