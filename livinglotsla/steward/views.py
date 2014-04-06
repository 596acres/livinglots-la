from django.core.urlresolvers import reverse
from django.views.generic import DetailView

from livinglots import get_lot_model
from livinglots_steward.views import BaseAddStewardNotificationView

from .forms import StewardNotificationForm
from .models import StewardNotification


class AddStewardNotificationView(BaseAddStewardNotificationView):
    content_type_model = get_lot_model()
    form_class = StewardNotificationForm

    def get_success_url(self):
        return reverse('steward:add_stewardnotification_success', kwargs={
            'pk': self.object.content_object.pk,
            'stewardnotification_pk': self.object.pk,
        })


class AddStewardNotificationSuccessView(DetailView):
    model = StewardNotification
    pk_url_kwarg = 'stewardnotification_pk'
    template_name = 'livinglots/steward/add_stewardnotification_success.html'
