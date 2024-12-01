from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models


class UserProfile(models.Model):
    USER_TYPE_CHOICES = [
        ('customer', 'Customer'),
        ('restaurant', 'Restaurant'),
    ]

    profile_picture = models.ImageField(upload_to="profile_pictures/", blank=True, null=True)
    name=models.CharField(max_length=100, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    phone_number = models.CharField(max_length=20, blank=True)
    email = models.CharField(max_length=255, blank=True)  
    created_at = models.DateTimeField(default=timezone.now) 
    user_type = models.CharField(max_length=50, choices=USER_TYPE_CHOICES)
  
    def __str__(self):
        return self.user.username
    
    
class RestaurantProfile(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    restaurant_name = models.CharField(max_length=100, blank=True)
    about = models.CharField(max_length=1000, blank=True)
    open_close_time = models.CharField(max_length=100, blank=True)
    restaurant_picture = models.ImageField(upload_to='restaurant_pictures/', blank=True, null=True)
    class Foodcate(models.TextChoices):
        CHOOSE_CATEGORY = "เลือกประเภทอาหาร", "เลือกประเภทอาหาร"
        RICE_AND_CURRY = "ข้าวราดแกง", "ข้าวราดแกง"
        MADE_TO_ORDER = "อาหารตามสั่ง", "อาหารตามสั่ง"
        DESSERT = "ขนมหวาน", "ขนมหวาน"
        WATER = "น้ำ", "น้ำ"
        NOODLES = "ก๋วยเตี๋ยว","ก๋วยเตี๋ยว"
        JAPANESE_FOOD = "อาหารญี่ปุ่น","อาหารญี่ปุ่น"
        SNACKS = "ของกินเล่น","ของกินเล่น"

    food_category = models.CharField(
        max_length=50,
        choices=Foodcate.choices,
        default=Foodcate.CHOOSE_CATEGORY
    )

    def __str__(self):
        return self.restaurant_name
    
class Menu(models.Model):
    restaurant_profile = models.ForeignKey(RestaurantProfile, on_delete=models.CASCADE, related_name='menus', default=1) 
    food_name = models.CharField(max_length=100, blank=True)
    about = models.CharField(max_length=1000, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    menu_picture = models.ImageField(upload_to='menu_picture/', null=True, blank=True)
    
    class Foodcate(models.TextChoices):
        CHOOSE_CATEGORY = "เลือกประเภทอาหาร", "เลือกประเภทอาหาร"
        RICE_AND_CURRY = "ข้าวราดแกง", "ข้าวราดแกง"
        MADE_TO_ORDER = "อาหารตามสั่ง", "อาหารตามสั่ง"
        DESSERT = "ขนมหวาน", "ขนมหวาน"
        WATER = "น้ำ", "น้ำ"
        NOODLES = "ก๋วยเตี๋ยว","ก๋วยเตี๋ยว"
        JAPANESE_FOOD = "อาหารญี่ปุ่น","อาหารญี่ปุ่น"
        SNACKS = "ของกินเล่น","ของกินเล่น"

    food_category = models.CharField(
        max_length=50,
        choices=Foodcate.choices,
        default=Foodcate.CHOOSE_CATEGORY
    )

    def __str__(self):
        return self.food_name  # แสดงชื่อเมนูจากฟิลด์ food_name

    
class PaymentMethod(models.Model):
    restaurant_profile = models.ForeignKey(
        RestaurantProfile, on_delete=models.CASCADE, related_name='payment', default=1)
    bank_name = models.CharField(max_length=100, blank=True)
    account_number = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.bank_name} : {self.account_number}"


class Order(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='orders')
    restaurant = models.ForeignKey(RestaurantProfile, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    order_date = models.DateTimeField(auto_now_add=True)
    pickup_time = models.DateTimeField(null=True, blank=True)  # เวลาที่ลูกค้าจะมารับ
    delivery_option_choices = [
        ('in_store', 'Pick up in store'),
        ('takeaway', 'Takeaway'),
    ]
    delivery_option = models.CharField(max_length=10, choices=delivery_option_choices, default='in_store')
    status_choices = [
        ('waiting_for_payment', 'Waiting for Payment'),
        ('paid', 'Paid'),
        ('cooking', 'Cooking'),
        ('completed', 'Completed'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='waiting_for_payment')

    def calculate_total(self):
        return sum(item.total_price for item in self.order_items.all())

    def __str__(self):
        return f"Order #{self.id} by {self.user_profile.user.username}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    restaurant_menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.restaurant_menu.food_name} x {self.quantity}"
   