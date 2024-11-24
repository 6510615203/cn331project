from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import UserProfile, RestaurantProfile, Menu


class ModelsTestCase(TestCase):
    def setUp(self):
        # สร้างข้อมูลตัวอย่างของ User, UserProfile, RestaurantProfile, และ Menu
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.user_profile = UserProfile.objects.create(
            user=self.user, name="Test User", user_type="restaurant"
        )
        self.restaurant = RestaurantProfile.objects.create(
            user_profile=self.user_profile,
            restaurant_name="ผัดไทใส่ใจ",
            food_category="อาหารไทย",
            about="อร่อย ฟิน",
            open_close_time="10:00 AM - 10:00 PM",
        )
        self.menu = Menu.objects.create(
            food_name="ผัดไทห่อไข่",
            food_category="อาหารจานหลัก",
            about="อร่อย",
            price=50.0,
        )

    def test_user_profile_str(self):
        # ทดสอบ __str__ ของ UserProfile
        self.assertEqual(str(self.user_profile), "testuser")

    def test_restaurant_profile_str(self):
        # ทดสอบ __str__ ของ RestaurantProfile
        self.assertEqual(str(self.restaurant), "ผัดไทใส่ใจ")

    def test_menu_str(self):
        # ทดสอบ __str__ ของ Menu
        self.assertEqual(str(self.menu), "ผัดไท")


class ViewsTestCase(TestCase):
    def setUp(self):
        # สร้างผู้ใช้, RestaurantProfile, และตั้งค่า client
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.user_profile = UserProfile.objects.create(
            user=self.user, name="Test User", user_type="restaurant"
        )
        self.restaurant = RestaurantProfile.objects.create(
            user_profile=self.user_profile,
            restaurant_name="ผัดไทใส่ใจ",
            food_category="อาหารไทย",
            about="อร่อย ฟิน",
            open_close_time="10:00 AM - 10:00 PM",
        )

    def test_index_view_authenticated(self):
        # ทดสอบการเข้าถึง index เมื่อผู้ใช้ล็อกอิน
        self.client.login(username="testuser", password="12345")
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index_restaurant.html")

    def test_index_view_unauthenticated(self):
        # ทดสอบกรณีผู้ใช้ไม่ได้ล็อกอิน
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 404)  # ไม่มีร้านค้าสำหรับผู้ใช้ที่ไม่ได้ล็อกอิน

    def test_manage_view_authenticated(self):
        # ทดสอบการเข้าถึง manage view เมื่อผู้ใช้ล็อกอิน
        self.client.login(username="testuser", password="12345")
        response = self.client.get(reverse("restaurant:manage"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manage_restaurant.html")

    def test_manage_view_unauthenticated(self):
        # ทดสอบการเข้าถึง manage view เมื่อผู้ใช้ไม่ได้ล็อกอิน
        response = self.client.get(reverse("restaurant:manage"))
        self.assertEqual(response.status_code, 403)  # Forbidden access

    def test_manage_view_update(self):
        # ทดสอบการอัปเดตข้อมูลร้าน
        self.client.login(username="testuser", password="12345")
        response = self.client.post(reverse("restaurant:manage"), {
            "restaurant_name": "Updated Restaurant",
            "food_category": "Updated Category",
        })
        self.assertEqual(response.status_code, 302)  # Redirect หลังแก้ไข
        self.restaurant.refresh_from_db()
        self.assertEqual(self.restaurant.restaurant_name, "Updated Restaurant")

    def test_about_view(self):
        # ทดสอบการเข้าถึง about view
        response = self.client.get(reverse("about"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "about_kinkorn.html")

    def test_order_list_view(self):
        # ทดสอบการเข้าถึง order list view
        response = self.client.get(reverse("order"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "order_list.html")

    def test_sales_report_view(self):
        # ทดสอบการเข้าถึง sales report view
        response = self.client.get(reverse("sales"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "sales.html")


class URLTestCase(TestCase):
    def test_urls(self):
        # ทดสอบว่า URL ทุกตัวสามารถเข้าถึงได้
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse("about"))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse("restaurant:manage"))
        self.assertEqual(response.status_code, 302)  # Requires login
