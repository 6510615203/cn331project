# Generated by Django 5.1.3 on 2024-11-17 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_restaurantprofile_restaurant_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='menu_picture',
            field=models.ImageField(blank=True, null=True, upload_to='menu_images/'),
        ),
    ]
