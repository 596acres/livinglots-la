from django.contrib import admin

from livinglots_owners.admin import BaseOwnerAdmin

from .models import Owner


class OwnerAdmin(BaseOwnerAdmin):
    pass


admin.site.register(Owner, OwnerAdmin)
