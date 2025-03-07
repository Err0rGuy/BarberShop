
from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from .validators import password_validator


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, first_name, last_name, phone_number, password, is_staff, is_superuser,
                     **extra_fields):
        if not phone_number:
            raise ValueError('The given phone number must be set')
        user = self.model(first_name=first_name, last_name=last_name, phone_number=phone_number,
                          is_staff=is_staff, is_active=True, date_joined=timezone.now()
                          , is_superuser=is_superuser, **extra_fields)
        if not extra_fields.get('no-password'):
            user.set_password(password)

        user.save(using=self._db)
        return user

    def create_user(self, phone_number=None, password=None,
                    **extra_fields):
        return self._create_user(phone_number=phone_number, password=password, is_staff=False, is_superuser=False,
                                 **extra_fields)

    def create_superuser(self, phone_number, password, **extra_fields):
        return self._create_user(phone_number=phone_number, password=password, is_superuser=True,
                                 is_staff=True
                                 , **extra_fields)

    def get_by_phone_number(self, phone_number):
        return self.get(**{'phone_number': phone_number})


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(_('first name'), max_length=50, null=False, blank=False)
    last_name = models.CharField(_('last name'), max_length=50, null=False, blank=False)
    phone_number = PhoneNumberField(_('phone number'), region='IR', unique=True, null=False, blank=False)
    password = models.CharField(_('password'), max_length=128, validators=[password_validator, ])
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('active'), default=True)
    date_joined = models.DateTimeField(_('date joined'), null=True, auto_now_add=True)
    avatar = models.ImageField(_('avatar'), upload_to='avatars/', null=True, blank=True)
    username = None
    objects = UserManager()
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.pk} --> {self.phone_number}"

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = 'users'

# Users Location model
class Location(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=False, related_name='location')
    province = models.CharField(max_length=25, blank=False)
    city = models.CharField(max_length=25, blank=False)
    zone = models.CharField(max_length=25, blank=False)

    def __str__(self):
        return f"province: {self.province}  city: {self.city}  zone: {self.zone}"

    class Meta:
        verbose_name = _('location')
        verbose_name_plural = _('locations')
        db_table = 'locations'


