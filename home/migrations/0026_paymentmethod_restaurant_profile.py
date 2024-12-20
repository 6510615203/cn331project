# Generated by Django 5.1.3 on 2024-11-24 06:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0025_paymentmethod_delete_foodcategory"),
    ]

    operations = [
        migrations.AddField(
            model_name="paymentmethod",
            name="restaurant_profile",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="payment",
                to="home.restaurantprofile",
            ),
        ),
    ]
