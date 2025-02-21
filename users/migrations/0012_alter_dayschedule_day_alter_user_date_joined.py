# Generated by Django 5.1.6 on 2025-02-21 20:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_remove_barberprofile_schedule_alter_user_date_joined_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dayschedule',
            name='day',
            field=models.PositiveSmallIntegerField(choices=[('Sunday', 'Sunday'), ('Saturday', 'Saturday'), ('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday')], default='Sunday', verbose_name='day'),
        ),
        migrations.AlterField(
            model_name='user',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2025, 2, 21, 20, 58, 4, 567462, tzinfo=datetime.timezone.utc), verbose_name='date joined'),
        ),
    ]
