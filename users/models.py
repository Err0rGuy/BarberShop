from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from .validators import password_validator


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, phone_number, password, is_staff, is_superuser,
                     **extra_fields):
        user = self.model(phone_number=phone_number,
                          is_staff=is_staff, is_active=True, date_joined=timezone.now()
                          , is_superuser=is_superuser, **extra_fields)
        if not extra_fields.get('no-password'):
            user.set_password(password)

        user.save(using=self._db)
        return user

    def create_user(self, phone_number=None, password=None,
                    **extra_fields):
        return self._create_user(phone_number, password=password, is_staff=False, is_superuser=False,
                                 **extra_fields)

    def create_superuser(self, phone_number, password, **extra_fields):
        return self._create_user(phone_number=phone_number, password=password, is_superuser=True,
                                 is_staff=True
                                 , **extra_fields)

    def get_by_phone_number(self, phone_number):
        return self.get(**{'phone_number': phone_number})


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(_('first name'), max_length=50, null=True)
    last_name = models.CharField(_('last name'), max_length=50, null=True)
    phone_number = PhoneNumberField(_('phone number'), region='IR', unique=True, null=True)
    password = models.CharField(_('password'), max_length=128, validators=[password_validator, ])
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('active'), default=True)
    date_joined = models.DateTimeField(_('date joined'), null=True, auto_now_add=True)
    location = models.OneToOneField('Location', null=True, on_delete=models.CASCADE)
    avatar = models.ImageField(_('avatar'), upload_to='avatars/', null=True, blank=True)
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return f"{self.pk} --> {self.phone_number}"

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['id']
        db_table = 'users'


class Barber(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE, null=True, related_name='barber')
    is_available = models.BooleanField(_('available'), default=True)
    max_reservation_days = models.SmallIntegerField(_('max reservation days'), default=7)
    reservation_gap = models.SmallIntegerField(_('reservation gap'), default=30)

    def __str__(self):
        return f"{self.pk} --> user: {self.user.pk}"

    class Meta:
        verbose_name = _('Barber')
        verbose_name_plural = _('barbers')
        ordering = ['id']
        db_table = 'barbers'


class UnAvailability(models.Model):
    barber = models.ForeignKey('Barber', on_delete=models.CASCADE, related_name='unavailability')
    start_date = models.DateTimeField(_('start date'), null=True)
    end_date = models.DateTimeField(_('end date'), null=True)
    reason = models.TextField(_('reason'), null=True, blank=True)

    def __str__(self):
        return f"from: {self.start_date}  to: {self.end_date}  barber: {self.barber.pk}"

    class Meta:
        verbose_name = _('UnAvailability')
        verbose_name_plural = _('UnAvailability')
        ordering = ['id']
        db_table = 'unavailability'


class WorkDay(models.Model):
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
    barber = models.ForeignKey(Barber, on_delete=models.CASCADE, null=True, related_name='work_days')

    def __str__(self):
        return f"day: {self.day}\tstart: {self.start_time}\tend: {self.end_time}"

    class Meta:
        verbose_name = _('workDay')
        verbose_name_plural = _('workDays')
        ordering = ['id']
        db_table = 'workDays'


class OffTime(models.Model):
    start_time = models.TimeField(_('start time'), null=True)
    end_time = models.TimeField(_('end time'), null=True)
    reason = models.TextField(_('reason'), null=True)
    day = models.ForeignKey(WorkDay, on_delete=models.CASCADE, null=True, related_name='off_times')

    def __str__(self):
        return f"from: {self.start_time}  to: {self.end_time}"

    class Meta:
        verbose_name = _('offTime')
        verbose_name_plural = _('offTimes')
        ordering = ['id']
        db_table = 'offTimes'


class Location(models.Model):
    longitude = models.DecimalField(_('longitude'), max_digits=10, decimal_places=5)
    latitude = models.DecimalField(_('latitude'), max_digits=10, decimal_places=5)

    def __str__(self):
        return f"longitude: {self.longitude}  latitude: {self.latitude}"

    class Meta:
        verbose_name = _('location')
        verbose_name_plural = _('locations')
        db_table = 'locations'


class Reservation(models.Model):
    STATUS_CHOICES = (
        ('ACCEPTED', 'accepted'),
        ('REJECTED', 'rejected'),
        ('WAITING', 'waiting'),
    )
    user = models.ForeignKey('User', on_delete=models.CASCADE, null=True, related_name='reservations')
    barber = models.ForeignKey('Barber', on_delete=models.CASCADE, null=True, related_name='reservations')
    date = models.DateTimeField(_('date'), null=True)
    accept_status = models.CharField(_('accept status'), choices=STATUS_CHOICES, default='waiting')

    class Meta:
        verbose_name = _('reservation')
        verbose_name_plural = _('reservations')
        db_table = 'reservations'


class Image(models.Model):
    image = models.ImageField(_('image'), upload_to='images/')
    barber = models.ForeignKey('Barber', on_delete=models.CASCADE, null=True, related_name='images')

    class Meta:
        verbose_name = _('image')
        verbose_name_plural = _('images')
        ordering = ['id']
        db_table = 'images'
