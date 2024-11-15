from django.urls import path
from home import views

urlpatterns = [
    path("",views.index, name="index"),
    path("about",views.about, name="about"),
    path("order",views.order, name="order"),
    path("yourorder",views.yourorder, name="yourorder"),
    path("register/", views.register, name="register"),
    path('choose_regis/', views.choose_regis, name='choose_regis'),
    path('login/', views.login_view, name='login'),
    path('index_restaurant/', views.index_restaurant, name='index_restaurant')
]