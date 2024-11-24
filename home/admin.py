from django.contrib import admin
from .models import UserProfile ,RestaurantProfile ,Menu,FoodCategory
# Register your models here.


class MenuInline(admin.TabularInline):
    model = Menu
    extra = 1
    fields = ('food_name', 'food_category', 'price', 'menu_picture')
    fk_name = 'restaurant_profile'

class RestaurantProfileAdmin(admin.ModelAdmin):
    inlines = [MenuInline]

admin.site.register(UserProfile)
admin.site.register(RestaurantProfile, RestaurantProfileAdmin)
admin.site.register(Menu)
admin.site.register(FoodCategory)
