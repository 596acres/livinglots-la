from django import forms
from django.utils.translation import ugettext_lazy as _

from livinglots_friendlyowners.forms import FriendlyOwnerFormMixin

from ladata.parcels.models import Parcel
from .models import FriendlyOwner


class ParcelsWidget(forms.HiddenInput):

    def value_from_datadict(self, data, files, name):
        value = data.get(name, None)
        if not value:
            return value
        return [value,]

    def render(self, name, value, attrs=None):
        try:
            value = ','.join(value)
        except Exception:
            value = value
        return super(ParcelsWidget, self).render(name, value, attrs=attrs)


class FriendlyOwnerForm(FriendlyOwnerFormMixin, forms.ModelForm):

    parcels = forms.ModelMultipleChoiceField(
        Parcel.objects.all(),
        error_messages={
            'required': _('Please select a parcel.'),
        },
        widget=ParcelsWidget()
    )

    class Meta:
        model = FriendlyOwner
        exclude = ('lot',)
