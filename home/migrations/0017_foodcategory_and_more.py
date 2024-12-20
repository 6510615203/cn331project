# Generated by Django 5.1.3 on 2024-11-23 14:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0016_restaurantprofile_user_profile'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FoodCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='restaurantprofile',
            name='restaurant_picture',
        ),
        migrations.AlterField(
            model_name='restaurantprofile',
            name='about',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='restaurantprofile',
            name='open_close_time',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='restaurantprofile',
            name='restaurant_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='restaurantprofile',
            name='user_profile',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='restaurantprofile',
            name='food_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.foodcategory'),
        ),
    ]
