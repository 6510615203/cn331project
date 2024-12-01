# Generated by Django 5.1.3 on 2024-12-01 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0031_order_payment_slip_alter_order_delivery_option'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('waiting_for_payment', 'Waiting for Payment'), ('paid', 'Paid'), ('completed', 'Completed')], default='pending', max_length=20),
        ),
    ]