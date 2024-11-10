from django.urls import path
from home import views

urlpatterns = [
    path("",views.index, name="index"),
    path("about",views.about, name="about"),
    path("order",views.order, name="order"),
    path("yourorder",views.yourorder, name="yourorder"),
    path("login",views.login, name="login")
]