# Generated by Django 5.0.2 on 2024-02-26 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0005_coupon'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='coupons',
            field=models.ManyToManyField(blank=True, to='hotel.coupon'),
        ),
    ]
