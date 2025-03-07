import datetime
from datetime import timedelta

from django.db.models import Q, Max

"""
Checking that reservation does not conflict with the barber absence time slot (UnAvailability).
< for example if the barber is traveling, no reservations will be recorded during this period. >
"""
def has_unavailability_overlap(reserve_date, barber):
    from .models import UnAvailability
    return UnAvailability.objects.filter(barber=barber).filter(
        Q(start_date__lte=reserve_date) & Q(end_date__gte=reserve_date)).exists()


"""
Checking that reservation does not conflict with the barber off time in a day (Off time).
< for example if the barber is asleep from 12:00 to 14:00, no reservations will be recorded during this period. >
"""
def is_in_off_time(reserve_date, barber):
    from .models import OffTime, WorkDay
    weekday = reserve_date.strftime('%A')
    workday = WorkDay.objects.filter(day=weekday, barber=barber).first()
    if not workday:
        return False
    reserve_date_hour = reserve_date.time()
    return OffTime.objects.filter(workday=workday).filter(
        Q(start_time__lte=reserve_date_hour) & Q(end_time__gte=reserve_date_hour)).exists()



"""
The barber determines how many days users can reserve in the next few day.
This validator will check this based on what barber has set.
< for example, the barber has set up for the next 30 days, 
    then user cannot book an appointment for next 31 days. >
"""
def invalid_max_reservation_days(reserve_date, barber):
    max_days = barber.max_reservation_days
    max_allowed_date = datetime.datetime.now() + datetime.timedelta(days=max_days)
    if reserve_date.date() > max_allowed_date.date():
        print("yes")
        return True
    return False


"""
The barber sets the interval between each reservations,
This validator will check this based on what barber has set.
< for example, if barber has set the time interval to 30 minutes,
and if someone has a reservation for 12:00,
    the acceptable times is 11:29 or 12:31 >
"""
def invalid_reservation_gap(reserve_date, barber):
    gap = timedelta(minutes=barber.reservation_gap)
    overlapping_reservations = barber.reservations.filter(date__date=reserve_date.date()).filter(
        Q(date__gte=reserve_date - gap) & Q(date__lte=reserve_date) | Q(date__lte=reserve_date + gap) & Q(
            date__gte=reserve_date)).exists()
    return overlapping_reservations
