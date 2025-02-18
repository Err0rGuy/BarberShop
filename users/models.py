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
        return self._create_user(username=username, phone_number=phone_number, password=password, is_superuser=True, is_staff=True
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

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone_number']
    objects = UserManager()

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['id']
        db_table = 'users'
