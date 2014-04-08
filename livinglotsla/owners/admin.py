from django import forms
from django.forms import ModelChoiceField
from django.contrib import admin

from autocomplete_light import ChoiceWidget

from livinglots_owners.admin import BaseOwnerAdmin, BaseOwnerContactAdmin

from .models import Owner, OwnerContact


class OwnerAdmin(BaseOwnerAdmin):
    pass


class OwnerContactAdminForm(forms.ModelForm):
    owner = ModelChoiceField(
        queryset=Owner.objects.all(),
        widget=ChoiceWidget('OwnerAutocomplete'),
    )

    class Meta:
        model = OwnerContact


class OwnerContactAdmin(BaseOwnerContactAdmin):
    form = OwnerContactAdminForm


admin.site.register(Owner, OwnerAdmin)
admin.site.register(OwnerContact, OwnerContactAdmin)
