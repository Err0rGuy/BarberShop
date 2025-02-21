# Generated by Django 5.1.6 on 2025-02-21 21:30

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_alter_appointment_user_alter_dayschedule_barber_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='barberprofile',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2025, 2, 21, 21, 30, 21, 974369, tzinfo=datetime.timezone.utc), verbose_name='date joined'),
        ),
    ]
