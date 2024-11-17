from django.contrib import admin
from .models import RestaurantProfile, UserProfile,Menu
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(RestaurantProfile)
admin.site.register(Menu)