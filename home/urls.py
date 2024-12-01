from django.urls import path
from django.conf import settings
from home import views
from django.conf.urls.static import static

urlpatterns = [
    path("",views.index, name="index"),
    path('accounts/login/', views.login_view, name='login'),  
    path("kinkorn",views.kinkorn, name="kinkorn"),
    path("about",views.about, name="about"),
    path("order",views.order, name="order"),
    path('your_order/', views.your_order, name='your_order'),
    path("register/", views.register, name="register"),
    path("restaurant_register/", views.restaurant_register, name="restaurant_register"),
    path("add_menu/", views.add_menu, name="add_menu"),
    path("welcome_registration/", views.welcome_registration, name="welcome_registration"),
    path('choose_regis/', views.choose_regis, name='choose_regis'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    #path('index_restaurant/', views.index_restaurant, name='index_restaurant')
    path('order/', views.restaurant_list, name='restaurant_list'), 
    path('menu/<int:restaurant_id>/', views.menu_list, name='menu_list'),  # ระบุ restaurant_id ใน URL
    path('menu/add/<int:menu_id>/', views.add_to_order, name='add_to_order'),
    path('delete_order/<int:order_id>/', views.delete_order, name='delete_order'),
    path('confirm_order/', views.confirm_order, name='confirm_order'),
    path('update_order_quantity/<int:order_id>/', views.update_order_quantity, name='update_order_quantity'),
    path('order_status/', views.order_status, name='order_status'),  # เพิ่ม URL นี้
    path('update_delivery_option/', views.update_delivery_option, name='update_delivery_option'),
    path('upload_payment_slip/<int:order_id>/', views.upload_payment_slip, name='upload_payment_slip'),
]

if settings.DEBUG:  # ใช้เฉพาะในโหมด debug (development server)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)