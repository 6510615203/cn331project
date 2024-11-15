
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models


from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone


class UserProfile(models.Model):
    USER_TYPE_CHOICES = [
        ('customer', 'Customer'),
        ('restaurant', 'Restaurant'),
    ]

    name=models.CharField(max_length=100, blank=True),
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    phone_number = models.CharField(max_length=20, blank=True)
    email = models.CharField(max_length=255, default="example@domain.com")  
    created_at = models.DateTimeField(default=timezone.now) 
    user_type = models.CharField(max_length=50, choices=USER_TYPE_CHOICES)
  
    def __str__(self):
        return self.user.username

