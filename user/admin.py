from django.urls import reverse
from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from user.models import User, Info


@admin.register(User)
class UserAdmin(BaseUserAdmin):

    list_filter = ('role', 'is_active')
    list_display = ('username', 'name', 'business', 'role')
    fieldsets = (('Site Roles', {'fields': ('role',)}),) + BaseUserAdmin.fieldsets

    @admin.display
    def business(self, obj):
        url = reverse('admin:user_info_change', args=[obj.info.id])
        return format_html('<a href="{}">{}</a>', url, obj.info.business_name)

    @admin.display(description='Full name')
    def name(self, obj):
        return obj.get_full_name()


@admin.register(Info)
class InfoAdmin(admin.ModelAdmin):
    list_filter = ('user__role',)
    list_display = ('business_name', 'username', 'pan')

    @admin.display(description='User')
    def username(self, obj: Info):
        url = reverse('admin:user_user_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)
