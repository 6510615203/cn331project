from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile, RestaurantProfile, Menu


class ModelTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="somtamkaiyang", password="passsomtam")
        self.profile = UserProfile.objects.create(user=self.user, name="Yingthai Jaingam", phone_number=66912345678, email="yingthaijai@gmail.com", user_type="restaurant")
        self.restaurant = RestaurantProfile.objects.create(restaurant_name="Somtam YingThai", food_category="Thai food", about="ขายส้มตำ ไก่ย่าง แซ่บๆ")
        self.menu = Menu.objects.create(food_name="ส้มตำไทย",food_category="ส้มตำ", about="ส้มตำไทย อร่อย ถูกใจวัยรุ่น" )

    def test_profile(self):
        self.assertEqual(self.profile.name, "Yingthai Jaingam")
        self.assertEqual(self.profile.phone_number, 66912345678)
        self.assertEqual(self.profile.email, "yingthaijai@gmail.com")
        self.assertEqual(self.profile.user_type, "restaurant")
        self.assertEqual(str(self.profile), "somtamkaiyang")

    def test_restaurant(self):
        self.assertEqual(self.restaurant.restaurant_name, "Somtam YingThai")
        self.assertEqual(self.restaurant.food_category, "Thai food")
        self.assertEqual(self.restaurant.about, "ขายส้มตำ ไก่ย่าง แซ่บๆ")
        self.assertEqual(str(self.restaurant), "Somtam YingThai")

    def test_menu(self):
        self.assertEqual(self.menu.food_name,"ส้มตำไทย")
        self.assertEqual(self.menu.food_category, "ส้มตำ")
        self.assertEqual(self.menu.about, "ส้มตำไทย อร่อย ถูกใจวัยรุ่น")
        self.assertEqual(str(self.menu), "ส้มตำไทย")
