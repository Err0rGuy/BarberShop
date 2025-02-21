# Generated by Django 5.1.6 on 2025-02-21 16:26

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_user_date_joined'),
    ]

    operations = [
        migrations.CreateModel(
            name='BarberProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('personal_image', models.ImageField(blank=True, null=True, upload_to='', verbose_name='personal image')),
                ('certification_image', models.ImageField(blank=True, null=True, upload_to='', verbose_name='certification image')),
                ('location', models.JSONField(blank=True, null=True, verbose_name='location')),
                ('schedule', models.JSONField(blank=True, null=True, verbose_name='schedule')),
            ],
            options={
                'verbose_name': 'Barber Profile',
                'verbose_name_plural': 'barbers profiles',
                'db_table': 'barbers_profiles',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='DaySchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')], default='Sunday', verbose_name='day')),
                ('start_time', models.TimeField(blank=True, null=True, verbose_name='start time')),
                ('end_time', models.TimeField(blank=True, null=True, verbose_name='end time')),
                ('is_available', models.BooleanField(default=True, verbose_name='available')),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2025, 2, 21, 16, 26, 42, 256992, tzinfo=datetime.timezone.utc), verbose_name='date joined'),
        ),
        migrations.AddField(
            model_name='user',
            name='barber_profile',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.barberprofile'),
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('reservation_time', models.DateTimeField(blank=True, null=True, verbose_name='reservation time')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('day_schedule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.dayschedule')),
            ],
            options={
                'verbose_name': 'Appointment',
                'verbose_name_plural': 'appointments',
                'db_table': 'appointments',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='OffDays',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True, verbose_name='date')),
                ('barber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.barberprofile')),
            ],
        ),
    ]
