# Generated by Django 5.0.2 on 2024-02-24 05:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0003_hotel_facebook_hotel_instagram_hotel_twitter_and_more'),
        ('userauth', '0002_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='payment_status',
            field=models.CharField(choices=[('1', ' PAID'), ('2', 'PENDING'), ('3', 'processing'), ('4', 'failed'), ('5', 'refunded'), ('6', 'NOT PAID'), ('7', 'CANCELLED')], default='NOT PAID', max_length=100),
        ),
        migrations.AlterField(
            model_name='booking',
            name='username',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='userauth.customer'),
        ),
    ]
