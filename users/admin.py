from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin

from users.models import *


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




@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('province', 'city', 'zone')
    search_fields = ('province', 'city', 'zone')
    list_filter = ('province', 'city', 'zone')
