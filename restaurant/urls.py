from django.urls import path
from . import views

app_name = "restaurant"
urlpatterns = [
    path('', views.index, name='index'),
    path('manage', views.manage, name='manage'),
    path('about_kinkorn', views.about, name='about'),
    path('order_list', views.order_list, name='order_list'),
    path('sales_report', views.sales_report, name='sales_report')
]
