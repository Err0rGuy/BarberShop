# Generated by Django 5.1.6 on 2025-03-02 10:25

import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0023_user_is_active_user_is_staff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='date',
            field=models.DateTimeField(null=True, verbose_name='date'),
        ),
        migrations.AlterField(
            model_name='unavailability',
            name='end_date',
            field=models.DateTimeField(null=True, verbose_name='end date'),
        ),
        migrations.AlterField(
            model_name='unavailability',
            name='start_date',
            field=models.DateTimeField(null=True, verbose_name='start date'),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=50, null=True, verbose_name='first name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=50, null=True, verbose_name='last name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, region='IR', unique=True, verbose_name='phone number'),
        ),
    ]
