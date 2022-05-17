from django.urls import reverse
from django.contrib import admin
from django.utils.html import format_html

from tax.models import Tax, TaxDue, State


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_ut', 'tax_rate', 'code')

    @admin.display
    def tax_rate(self, obj):
        return f'{obj.tax}%'


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ('due_date', 'payer', 'updated_on')

    @admin.display
    def due_date(self, obj: Tax):
        return obj.active_due.due_date

    @admin.display
    def payer(self, obj: Tax):
        url = reverse('admin:user_user_change', args=(obj.payer.id,))
        return format_html(f'<a href="{url}">{obj.payer.username}</a>')


admin.site.register(TaxDue)
