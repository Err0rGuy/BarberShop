# Generated by Django 5.1.6 on 2025-03-06 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Barber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_available', models.BooleanField(default=True, verbose_name='available')),
                ('max_reservation_days', models.SmallIntegerField(default=7, verbose_name='max reservation days')),
                ('reservation_gap', models.SmallIntegerField(default=30, verbose_name='reservation gap')),
            ],
            options={
                'verbose_name': 'Barber',
                'verbose_name_plural': 'barbers',
                'db_table': 'barbers',
            },
        ),
        migrations.CreateModel(
            name='ImageGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/', verbose_name='image')),
            ],
            options={
                'verbose_name': 'image',
                'verbose_name_plural': 'images',
                'db_table': 'images',
            },
        ),
        migrations.CreateModel(
            name='OffTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField(null=True, verbose_name='start time')),
                ('end_time', models.TimeField(null=True, verbose_name='end time')),
                ('reason', models.TextField(blank=True, null=True, verbose_name='reason')),
            ],
            options={
                'verbose_name': 'offTime',
                'verbose_name_plural': 'offTimes',
                'db_table': 'offTimes',
            },
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(verbose_name='date')),
                ('accept_status', models.CharField(choices=[('ACCEPTED', 'accepted'), ('REJECTED', 'rejected'), ('WAITING', 'waiting')], default='waiting', verbose_name='accept status')),
            ],
            options={
                'verbose_name': 'reservation',
                'verbose_name_plural': 'reservations',
                'db_table': 'reservations',
            },
        ),
        migrations.CreateModel(
            name='UnAvailability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(verbose_name='start date')),
                ('end_date', models.DateTimeField(verbose_name='end date')),
                ('reason', models.TextField(blank=True, verbose_name='reason')),
            ],
            options={
                'verbose_name': 'UnAvailability',
                'verbose_name_plural': 'UnAvailability',
                'db_table': 'unavailability',
            },
        ),
        migrations.CreateModel(
            name='WorkDay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(choices=[('Sunday', 'Sunday'), ('Saturday', 'Saturday'), ('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday')], verbose_name='day')),
                ('start_time', models.TimeField(verbose_name='start time')),
                ('end_time', models.TimeField(verbose_name='end time')),
            ],
            options={
                'verbose_name': 'workDay',
                'verbose_name_plural': 'workDays',
                'db_table': 'workDays',
            },
        ),
    ]
