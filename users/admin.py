from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin
from users.models import User, BarberProfile, Appointment, DaySchedule, OffDays


class ProfileInline(admin.TabularInline):
    model = BarberProfile
    extra = 0

class OffDaysInline(admin.TabularInline):
    model = OffDays
    extra = 0

class DayScheduleInline(admin.TabularInline):
    model = DaySchedule
    extra = 0

class AppointmentInline(admin.TabularInline):
    model = Appointment
    extra = 0

@admin.register(User)
class UserAdmin(ImportExportModelAdmin, UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password', 'has_barber_profile')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'phone_number')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    inlines = (AppointmentInline, )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'phone_number', 'password1', 'password2'),
        }),
    )

    list_display = ('username', 'phone_number', 'is_staff')
    search_fields = ('username',)
    ordering = ('id',)


@admin.register(BarberProfile)
class BarberAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'location')
    inlines = (DayScheduleInline, OffDaysInline)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'appointment_date')


@admin.register(DaySchedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('day', 'start_time', 'end_time', 'is_available', 'barber_id')


@admin.register(OffDays)
class OffDaysAdmin(admin.ModelAdmin):
    list_display = ('barber', 'date')
