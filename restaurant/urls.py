from django.urls import path,include
from . import views

app_name = 'restaurant'

urlpatterns = [
    path('', views.index, name='index'), 
   
]
