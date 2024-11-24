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
    
class FoodCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)  # ชื่อประเภทอาหาร (ไม่ซ้ำ)
    def __str__(self):
        return self.name
    
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
    price = models.DecimalField(max_digits=10,     
        decimal_places=2, default=0.00)
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
        return self.food_name


    