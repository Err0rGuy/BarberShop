from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin

from users.models import *


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
    model = Image
    extra = 0


@admin.register(User)
class UserAdmin(ImportExportModelAdmin, UserAdmin):
    fieldsets = (
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'phone_number', 'location', 'avatar')}),
        (_('Permissions'), {'fields': ('is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    inlines = []

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'phone_number', 'password1', 'password2'),
        }),
    )

    list_display = ('first_name', 'last_name', 'phone_number', 'is_superuser', 'date_joined')
    search_fields = ('phone_number', 'first_name', 'last_name')
    list_filter = ('is_superuser',)
    ordering = ('id',)


@admin.register(Barber)
class BarberAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'is_available')
    inlines = (WorkDaysInline, UnAvailabilityInline, ImagesInline)


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'barber_id', 'date', 'accept_status')
    search_fields = ('date',)


@admin.register(WorkDay)
class WorkDaysAdmin(admin.ModelAdmin):
    list_display = ('day', 'start_time', 'end_time', 'barber_id')
    inlines = (OffTimesInline,)
    list_filter = ('day',)
