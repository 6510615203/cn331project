from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "restaurant"

urlpatterns = [
    path('', views.index, name='index'),
    path('manage', views.manage, name='manage'),
    path('about_kinkorn', views.about, name='about'),
    path('order_list', views.order_list, name='order_list'),
    path('sales_report', views.sales_report, name='sales_report'),
    path('edit_menu_payment', views.edit_menu_payment, name='edit_menu_payment'),
    path('add_menu_res', views.add_menu_res, name='add_menu_res'),
    path('add_payment', views.add_payment, name='add_payment'),
]

if settings.DEBUG:  # ใช้เฉพาะในโหมด debug (development server)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)