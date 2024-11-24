# Generated by Django 5.1.3 on 2024-11-24 12:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0027_alter_paymentmethod_restaurant_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentmethod',
            name='restaurant_profile',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='payment', to='home.restaurantprofile'),
        ),
    ]
