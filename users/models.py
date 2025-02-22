import random

from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from .validators import password_validator


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, phone_number, password, is_staff, is_superuser,
                     **extra_fields):
        if not username:
            raise ValueError("The given username must be set")
        user = self.model(username=username, phone_number=phone_number,
                          is_staff=is_staff, is_active=True, date_joined=timezone.now()
                          , is_superuser=is_superuser, **extra_fields)
        if not extra_fields.get('no-password'):
            user.set_password(password)

        user.save(using=self._db)
        return user

    def create_user(self, username=None, phone_number=None, password=None,
                    **extra_fields):
        if not username:
            if phone_number:
                username = random.choice('abcdefghijklmnopqrstuvwxyz') + str(phone_number)[-7:]
            while User.objects.filter(username=username).exists():
                username += str(random.randrange(10, 99))
        return self._create_user(username, phone_number, password, False, False,
                                 **extra_fields)

    def create_superuser(self, username, phone_number, password, **extra_fields):
        return self._create_user(username=username, phone_number=phone_number, password=password, is_superuser=True,
                                 is_staff=True
                                 , **extra_fields)

    def get_by_phone_number(self, phone_number):
        return self.get(**{'phone_number': phone_number})


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(_('first name'), max_length=50, blank=True, null=True)
    last_name = models.CharField(_('last name'), max_length=50, blank=True, null=True)
    username = models.CharField(_('username'), max_length=150, unique=True)
    phone_number = PhoneNumberField(_('phone number'), region='IR', unique=True, blank=True, null=True)
    password = models.CharField(_('password'), max_length=128, validators=[password_validator, ])
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('active'), default=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now())
    has_barber_profile = models.BooleanField(_('has barber profile'), default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone_number']
    objects = UserManager()

    def __str__(self):
        return f"username: {self.username}"

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['id']
        db_table = 'users'

# Identifying barbers by this profile
class BarberProfile(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE, null=True, related_name='profile')
    personal_image = models.ImageField(_('personal image'), null=True, blank=True, upload_to='personals/')
    certification_image = models.ImageField(_('certification image'), null=True, upload_to='certifications/')
    location = models.JSONField(_('location'), null=True)

    def set_location(self, state, city, address):
        self.location = Location(state, city, address).to_dict()

    def get_location(self) -> 'Location':
        return Location.from_dict(self.location)

    def __str__(self):
        return f"barber: {self.user.username}"

    class Meta:
        verbose_name = _('Barber Profile')
        verbose_name_plural = _('barbers profiles')
        ordering = ['id']
        db_table = 'barbers_profiles'

# Setting start and end worktime for week days for barber
class DaySchedule(models.Model):
    DAY_CHOICES = (
        ('Sunday', 'Sunday'),
        ('Saturday', 'Saturday'),
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
    )
    day = models.CharField(_('day'), choices=DAY_CHOICES, null=True)
    start_time = models.TimeField(_('start time'), null=True)
    end_time = models.TimeField(_('end time'), null=True)
    is_available = models.BooleanField(_('available'), default=True)
    barber = models.ForeignKey(BarberProfile, on_delete=models.CASCADE, null=True, related_name='days_schedules')

    def __str__(self):
        return f"day: {self.day}\tstart: {self.start_time}\tend: {self.end_time}"

    class Meta:
        verbose_name = _('Day Schedule')
        verbose_name_plural = _('days schedule')
        ordering = ['id']
        db_table = 'days_schedules'

# Setting work off days for barber
class OffDays(models.Model):
    barber = models.ForeignKey(BarberProfile, on_delete=models.CASCADE, null=True, related_name='off_days')
    date = models.DateField(_('date'), null=True)

    def __str__(self):
        return f"barber: {self.barber.user.username}\tdate: {self.date}"

    class Meta:
        verbose_name = _('Off Day')
        verbose_name_plural = _('Off Days')
        ordering = ['id']
        db_table = 'off_days'

# Setting appointment date and time by user
class Appointment(models.Model):
    barber = models.ForeignKey(BarberProfile, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    appointment_date = models.DateTimeField(_('appointment date'), null=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, null=True, related_name='appointments')

    def __str__(self):
        return f"user: {self.user.username}\tdate: {self.appointment_date}"

    class Meta:
        verbose_name = _('Appointment')
        verbose_name_plural = _('appointments')
        ordering = ['id']
        db_table = 'appointments'

# Barber Location
class Location:
    def __init__(self, state, city, address):
        self.state = state
        self.city = city
        self.address = address

    @property
    def get_state(self):
        return self.state

    @property
    def get_city(self):
        return self.city

    @property
    def get_address(self):
        return self.address

    def to_dict(self):
        return {'state': self.state, 'city': self.city, 'address': self.address}

    @classmethod
    def from_dict(cls, data):
        return cls(data['state'], data['city'], data['address'])

    def __str__(self):
        return f'{self.state} {self.city} {self.address}'
