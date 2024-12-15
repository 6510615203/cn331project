from decimal import Decimal
from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile, RestaurantProfile, Menu, PaymentMethod, Order, OrderItem


class ModelTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="somtamkaiyang", password="passsomtam")
        self.profile = UserProfile.objects.create(user=self.user, name="Yingthai Jaingam", phone_number=66912345678, email="yingthaijai@gmail.com", user_type="restaurant")
        self.restaurant = RestaurantProfile.objects.create(restaurant_name="Somtam YingThai", food_category="Thai food", about="ขายส้มตำ ไก่ย่าง แซ่บๆ")
        self.menu = Menu.objects.create(food_name="ส้มตำไทย",food_category="ส้มตำ", about="ส้มตำไทย อร่อย ถูกใจวัยรุ่น", price=50.00 )
        self.payment_method = PaymentMethod.objects.create(restaurant_profile=self.restaurant, bank_name="KBank", account_number="123456789")
        self.order = Order.objects.create(user_profile=self.profile, restaurant=self.restaurant, total_price=0.00, status="waiting_for_payment")
        self.order_item = OrderItem.objects.create(order=self.order, restaurant_menu=self.menu, quantity=2, total_price=self.menu.price * 2)
        self.order.total_price = self.order.calculate_total()
        self.order.save()

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

    def test_is_restaurant_user_type(self):
        self.assertTrue(self.profile.is_restaurant())

    def test_payment_method_str(self):
        self.assertEqual(str(self.payment_method), "KBank : 123456789")

    def test_order_item_str(self):
        self.assertEqual(str(self.order_item), "ส้มตำไทย x 2")

    def test_order_str(self):
        self.assertEqual(str(self.order), "Order #1 by somtamkaiyang")

    def test_order_status(self):
        self.assertEqual(self.order.status, "waiting_for_payment")

    def test_order_item_creation(self):
        self.assertEqual(self.order.order_items.count(), 1)
        self.assertEqual(self.order_item.total_price, Decimal('100.00'))



