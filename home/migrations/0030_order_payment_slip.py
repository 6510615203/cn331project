# Generated by Django 5.1.3 on 2024-12-07 03:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0029_order_orderitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_slip',
            field=models.ImageField(blank=True, null=True, upload_to='payment_slips/'),
        ),
    ]
