from rest_framework.exceptions import ValidationError
from django.db import models
from django.db.models import UniqueConstraint
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
from users.models import User
from .validators import has_unavailability_overlap, is_in_off_time, invalid_max_reservation_days, \
    invalid_reservation_gap, is_in_working_hours


class Barber(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_available = models.BooleanField(_('available'), default=True, blank=False)
    max_reservation_days = models.SmallIntegerField(_('max reservation days'), default=7, blank=False)
    reservation_gap = models.SmallIntegerField(_('reservation gap'), default=30, blank=False)

    def __str__(self):
        return f"{self.pk} --> user: {self.user.pk}"

    def clean(self):
        if self.max_reservation_days > 30:
            raise ValidationError(_('Max reservation days cannot be greater than 30'))

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Barber')
        verbose_name_plural = _('barbers')
        db_table = 'barbers'

"""
Set a time period when the barber is unavailable.
< for example barber is traveling from beginning to the end of this month. >
"""
class UnAvailability(models.Model):
    barber = models.ForeignKey('Barber', on_delete=models.CASCADE, null=True, related_name='unavailability')
    start_date = models.DateTimeField(_('start date'), blank=False)
    end_date = models.DateTimeField(_('end date'), blank=False)
    reason = models.TextField(_('reason'), blank=True)

    def __str__(self):
        return f"from: {self.start_date}  to: {self.end_date}  barber: {self.barber.pk}"

    def clean(self):
        if self.start_date < now():
            raise ValidationError(_('Start date cannot be before now'))
        if self.start_date > self.end_date:
            raise ValidationError(_('start date must be before end date'))

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('UnAvailability')
        verbose_name_plural = _('UnAvailability')
        db_table = 'unavailability'


"""
Setting a schedule for every day of the week for the barber.
< for example start and the end time on Monday, also off times for rest or anything else... >
"""
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
    day = models.CharField(_('day'), choices=DAY_CHOICES, null=False, blank=False)
    start_time = models.TimeField(_('start time'), blank=False)
    end_time = models.TimeField(_('end time'), blank=False)
    barber = models.ForeignKey(Barber, on_delete=models.CASCADE, related_name='workdays')

    def __str__(self):
        return f"day: {self.day}\tstart: {self.start_time}\tend: {self.end_time}"

    def clean(self):
        if self.start_time > self.end_time:
            raise ValidationError(_('start time must be before end time'))

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('workDay')
        verbose_name_plural = _('workDays')
        db_table = 'workDays'
        constraints = [
            UniqueConstraint(fields=['barber', 'day'], name='unique_barber_day'),
        ]


"""
Setting off times for a week day.
< for example the barber is asleep from 12:00(start time) to 14:00(end time) >
"""
class OffTime(models.Model):
    start_time = models.TimeField(_('start time'), null=False, blank=False)
    end_time = models.TimeField(_('end time'), null=False, blank=False)
    reason = models.TextField(_('reason'), null=True, blank=True)
    workday = models.ForeignKey(WorkDay, on_delete=models.CASCADE, related_name='off_times')

    def __str__(self):
        return f"from: {self.start_time}  to: {self.end_time}"

    def clean(self):
        if self.start_time > self.end_time:
            raise ValidationError(_('start time must be before end time'))

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('offTime')
        verbose_name_plural = _('offTimes')
        db_table = 'offTimes'


"""
Just a model for implementing reservations
"""
class Reservation(models.Model):
    STATUS_CHOICES = (
        ('accepted', 'accepted'),
        ('rejected', 'rejected'),
        ('waiting', 'waiting'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations', blank=False)
    barber = models.ForeignKey('Barber', on_delete=models.CASCADE, related_name='reservations', null=False, blank=False)
    date = models.DateTimeField(_('date'), blank=False)
    status = models.CharField(_('status'), choices=STATUS_CHOICES, default='waiting')

    def clean(self):
        if self.date < now():
            raise ValidationError(_('The reservation time cannot be later than the present'))
        if is_in_working_hours(self.date, self.barber):
            raise ValidationError(_('Reservation time is not during working hours'))
        if has_unavailability_overlap(self.date, self.barber):
            raise ValidationError(_('date overlaps with barber unavailability!'))
        if is_in_off_time(self.date, self.barber):
            raise ValidationError(_('date is in off-time!'))
        if invalid_max_reservation_days(self.date, self.barber):
            raise ValidationError(_(f'only can reserve for the next {self.barber.max_reservation_days} days!'))
        if invalid_reservation_gap(self.date, self.barber):
            raise ValidationError(_('this time has already been reserved!'))

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('reservation')
        verbose_name_plural = _('reservations')
        db_table = 'reservations'


"""
For barber to upload images including work samples and shop photos.
"""
class ImageGallery(models.Model):
    image = models.ImageField(_('image'), upload_to='images/', blank=False)
    barber = models.ForeignKey('Barber', on_delete=models.CASCADE, related_name='images')

    class Meta:
        verbose_name = _('image')
        verbose_name_plural = _('images')
        db_table = 'images'
