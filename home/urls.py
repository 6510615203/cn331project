from django.urls import path
from django.conf import settings
from home import views
from django.conf.urls.static import static

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

if settings.DEBUG:  # ใช้เฉพาะในโหมด debug (development server)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)