from django.contrib import admin

from django_monitor.admin import MonitorAdmin

from livinglots_friendlyowners.admin import FriendlyOwnerAdminMixin

from .models import FriendlyOwner


class FriendlyOwnerAdmin(FriendlyOwnerAdminMixin, MonitorAdmin):
    pass


admin.site.register(FriendlyOwner, FriendlyOwnerAdmin)
