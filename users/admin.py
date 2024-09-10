from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('userID', 'email', 'name', 'phone_number', 'is_owner', 'is_staff', 'is_active')
    list_filter = ['is_active', 'is_owner', 'is_staff']
    ordering = ('userID',)
    search_fields = ('userID', 'email', 'name', 'phone_number')
    fieldsets = (
        (None, {'fields': ('userID', 'email', 'password')}),
        ('Personal Info', {'fields': ('name', 'phone_number', 'address', 'profile_picture')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_owner')}),
        ('Important Dates', {'fields': ('last_login', 'make_date')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('userID', 'email', 'name', 'phone_number', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
