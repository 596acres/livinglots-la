from django.contrib import admin

from livinglots_lots.admin import BaseLotAdmin

from .models import Lot


class LotAdmin(BaseLotAdmin):
    list_display = ('pk', 'address_line1', 'city', 'name', 'known_use',)
    fieldsets = BaseLotAdmin.fieldsets + (
        ('Ownership', {
            'fields': ('owner',),
        }),
    )


admin.site.unregister(Lot)
admin.site.register(Lot, LotAdmin)
