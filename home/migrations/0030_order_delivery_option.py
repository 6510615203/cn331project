# Generated by Django 5.1.3 on 2024-12-01 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0029_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_option',
            field=models.CharField(choices=[('in_store', 'รับที่ร้าน'), ('takeaway', 'ใส่กล่อง')], default='in_store', max_length=10),
        ),
    ]