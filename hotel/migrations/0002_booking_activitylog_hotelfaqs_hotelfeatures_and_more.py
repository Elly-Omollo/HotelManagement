# Generated by Django 5.0.2 on 2024-02-12 08:18

import django.db.models.deletion
import shortuuid.django_fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0001_initial'),
        ('userauth', '0002_customer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=200)),
                ('phone', models.CharField(max_length=100)),
                ('before_discount', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('payable', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('saved', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('check_in_date', models.DateField()),
                ('check_out_date', models.DateField()),
                ('total_days', models.PositiveIntegerField(default=0)),
                ('number_adults', models.PositiveIntegerField(default=1)),
                ('num_children', models.PositiveIntegerField(default=0)),
                ('checked_in', models.BooleanField(default=False)),
                ('checked_out', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('checked_in_tracker', models.BooleanField(default=False)),
                ('checked_out_tracker', models.BooleanField(default=False)),
                ('payment_status', models.CharField(choices=[('1', ' PAID'), ('2', 'PENDING'), ('3', 'processing'), ('4', 'failed'), ('5', 'refunded'), ('6', 'unpaid'), ('7', 'CANCELLED')], default='NOT PAID', max_length=100)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('success_id', models.CharField(max_length=100)),
                ('bookingid', shortuuid.django_fields.ShortUUIDField(alphabet='abcdefghijklmnopqrstuvwxyz123', length=6, max_length=20, prefix='', unique=True)),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='hotel.hotel')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userauth.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Activitylog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guest_out', models.DateTimeField()),
                ('guest_in', models.DateTimeField()),
                ('activity_description', models.TextField(blank=True, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='hotel.booking')),
            ],
        ),
        migrations.CreateModel(
            name='HotelFaqs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=1000)),
                ('answer', models.CharField(blank=True, max_length=1000, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.hotel')),
            ],
            options={
                'verbose_name_plural': 'FAQs',
            },
        ),
        migrations.CreateModel(
            name='HotelFeatures',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icon_type', models.CharField(choices=[('Bootstrap', 'Bootstrap'), ('Fontawesome', 'Fontawesome'), ('Sanserif', 'Sanserif')], default='Bootstrap', max_length=100)),
                ('icon', models.CharField(blank=True, max_length=100, null=True)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.hotel')),
            ],
            options={
                'verbose_name_plural': 'hotel features',
            },
        ),
        migrations.CreateModel(
            name='HotelGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(upload_to='hotel_gallery')),
                ('hgid', shortuuid.django_fields.ShortUUIDField(alphabet='abcdefghijklmnopqrstuvwxyz123', length=6, max_length=20, prefix='', unique=True)),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.hotel')),
            ],
            options={
                'verbose_name_plural': 'hotel gallery',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_number', models.CharField(max_length=100)),
                ('is_available', models.BooleanField(default=True)),
                ('room_id', shortuuid.django_fields.ShortUUIDField(alphabet='abcdefghijklmnopqrstuvwxyz123', length=6, max_length=20, prefix='', unique=True)),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.hotel')),
            ],
            options={
                'verbose_name_plural': 'Rooms',
            },
        ),
        migrations.AddField(
            model_name='booking',
            name='room',
            field=models.ManyToManyField(to='hotel.room'),
        ),
        migrations.CreateModel(
            name='RoomType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_type', models.CharField(blank=True, max_length=100, null=True)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('number_of_beds', models.PositiveIntegerField(default=1)),
                ('room_capsity', models.PositiveIntegerField(default=0)),
                ('roomtypeid', shortuuid.django_fields.ShortUUIDField(alphabet='abcdefghijklmnopqrstuvwxyz123', length=6, max_length=20, prefix='', unique=True)),
                ('slug', models.CharField(blank=True, max_length=100, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.hotel')),
            ],
            options={
                'verbose_name_plural': 'Room Type',
            },
        ),
        migrations.AddField(
            model_name='room',
            name='room_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.roomtype'),
        ),
        migrations.AddField(
            model_name='booking',
            name='room_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='hotel.roomtype'),
        ),
        migrations.CreateModel(
            name='StaffOnDuty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('staff_id', shortuuid.django_fields.ShortUUIDField(alphabet='abcdefghijklmnopqrstuvwxyz123', length=6, max_length=20, prefix='', unique=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('phone', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(blank=True, max_length=1000, null=True)),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='hotel.booking')),
            ],
        ),
    ]