# Generated by Django 5.1.6 on 2025-03-06 17:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('barbers', '0006_alter_offtime_end_time_alter_offtime_start_time_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reservation',
            old_name='accept_status',
            new_name='status',
        ),
    ]
