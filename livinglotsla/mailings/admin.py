from django.contrib import admin

from .models import DaysAfterAddedMailing


class DaysAfterAddedMailingAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_checked', 'days_after_added',)


admin.site.register(DaysAfterAddedMailing, DaysAfterAddedMailingAdmin)
