from django.contrib import admin
from .models import FoodCategory, UserProfile ,RestaurantProfile ,Menu
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(RestaurantProfile)
admin.site.register(Menu)
admin.site.register(FoodCategory)