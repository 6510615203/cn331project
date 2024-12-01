from django.urls import path
from django.conf import settings
from home import views
from django.conf.urls.static import static

urlpatterns = [
    path("",views.index, name="index"),
    path("kinkorn",views.kinkorn, name="kinkorn"),
    path("about",views.about, name="about"),
    path("order",views.order, name="order"),
    path("yourorder",views.yourorder, name="yourorder"),
    path("register/", views.register, name="register"),
    path("restaurant_register/", views.restaurant_register, name="restaurant_register"),
    path("add_menu/", views.add_menu, name="add_menu"),
    path("welcome_registration/", views.welcome_registration, name="welcome_registration"),
    path('choose_regis/', views.choose_regis, name='choose_regis'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    #path('index_restaurant/', views.index_restaurant, name='index_restaurant')
    path('order/', views.restaurant_list, name='restaurant_list'), 
    path('menu/<int:restaurant_id>/', views.menu_list, name='menu_list'),
    path('order_status/', views.order_status, name='order_status'),
    path('upload_payment_slip/<int:order_id>/', views.upload_payment_slip, name='upload_payment_slip'),
    path('your_order/', views.your_order, name='your_order'),
    path('order_confirmation/', views.order_confirmation, name='order_confirmation'),
    
]   

if settings.DEBUG:  # ใช้เฉพาะในโหมด debug (development server)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)