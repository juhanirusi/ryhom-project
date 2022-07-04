from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import Account

admin.site.site_header = "Ryhom"
admin.site.site_title  =  "Ryhom Admin"
admin.site.index_title  =  "Ryhom Admin Dashboard"


@admin.action(description='Activate Account(s)')
def make_active(modeladmin, request, queryset):
    queryset.update(is_active = True)
    messages.success(request, "Selected Account(s) Marked As Active!")


@admin.action(description='Deactivate Account(s)')
def make_inactive(modeladmin, request, queryset):
    queryset.update(is_active = False)
    messages.success(request, "Selected Account(s) Marked As Inactive!")


class UserAdmin(BaseUserAdmin):
    """Define the admin page customization."""
    ordering = ['id']
    list_display = ['email', 'username', 'name', 'is_active']
    list_filter = ('is_active', 'is_superuser', 'is_staff', 'gender',)
    search_fields = ['email', 'name', 'username']
    actions = [make_active, make_inactive]

    fieldsets = (
        (_('Account Info'), {'fields': (
            'email', 'username', 'slug', 'password')}
        ),
        (_('Personal Info'), {'fields': (
            'name', 'gender', 'birthday', 'profile_image', 'bio', 'website')}
        ),
        (_('Permissions'), {'fields': (
            'is_active', 'is_staff', 'is_superuser',)}
        ),
        (_('Important Dates'), {'fields': ('last_login', 'date_joined',)}),
    )

    readonly_fields = ['last_login', 'date_joined']

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_superuser',
            ),
        }),
    )

admin.site.register(Account, UserAdmin)
