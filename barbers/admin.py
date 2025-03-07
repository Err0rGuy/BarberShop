from django.contrib import admin
from .models import *

class OffTimesInline(admin.TabularInline):
    model = OffTime
    extra = 0


class WorkDaysInline(admin.TabularInline):
    model = WorkDay
    extra = 0


class UnAvailabilityInline(admin.TabularInline):
    model = UnAvailability
    extra = 0


class ImagesInline(admin.TabularInline):
    model = ImageGallery
    extra = 0


@admin.register(Barber)
class BarberAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'is_available')
    inlines = (WorkDaysInline, UnAvailabilityInline, ImagesInline)


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'barber_id', 'date', 'status')
    search_fields = ('date',)


@admin.register(WorkDay)
class WorkDaysAdmin(admin.ModelAdmin):
    list_display = ('day', 'start_time', 'end_time', 'barber_id')
    inlines = (OffTimesInline,)
    list_filter = ('day',)
