from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import UserProfile, RestaurantProfile, Menu
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

"""
    def test_restaurant_register_create(self):
        self.client.login(username="sushinumberome", password="Pass@sushi1")
        data = {
            "restaurant_name": "ซูชิที่หนึ่ง",
            "food_category": "อาหารญี่ปุ่น",
            "about": "ซูชิญี่ปุ่น",
            "open_close_time": "10.00 - 16.00"
        }
        response = self.client.post(reverse("restaurant_register"), data)
        expected_url = reverse("add_menu") + "?restaurant_name=ซูชิที่หนึ่ง"
        self.assertRedirects(response, expected_url)
"""
