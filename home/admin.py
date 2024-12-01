from django.contrib import admin
from .models import UserProfile ,RestaurantProfile ,Menu, PaymentMethod, Order
# Register your models here.


class MenuInline(admin.TabularInline):
    model = Menu
    extra = 1
    fields = ('food_name', 'food_category', 'price', 'menu_picture')
    fk_name = 'restaurant_profile'

class PaymentInline(admin.TabularInline):
    model = PaymentMethod
    extra = 1
    fileds = ('bank_name', 'account_number')
    fk_name = 'restaurant_profile'

class RestaurantProfileAdmin(admin.ModelAdmin):
    inlines = [MenuInline, PaymentInline]

admin.site.register(UserProfile)
admin.site.register(RestaurantProfile, RestaurantProfileAdmin)
admin.site.register(Menu)
admin.site.register(PaymentMethod)
admin.site.register(Order)
