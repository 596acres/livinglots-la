from django.core.urlresolvers import reverse
from django.views.generic import DetailView

from livinglots import get_lot_model
from livinglots_groundtruth.views import BaseAddGroundtruthRecordView

from .forms import GroundtruthRecordForm
from .models import GroundtruthRecord


class AddGroundtruthRecordView(BaseAddGroundtruthRecordView):
    content_type_model = get_lot_model()
    form_class = GroundtruthRecordForm

    def get_form_kwargs(self):
        kwargs = super(AddGroundtruthRecordView, self).get_form_kwargs()
        kwargs.update({ 'user': self.request.user })
        return kwargs

    def get_success_url(self):
        return reverse('groundtruth:add_groundtruthrecord_success', kwargs={
            'pk': self.object.content_object.pk,
            'groundtruthrecord_pk': self.object.pk,
        })


class AddGroundtruthRecordSuccessView(DetailView):
    model = GroundtruthRecord
    pk_url_kwarg = 'groundtruthrecord_pk'
    template_name = 'livinglots/groundtruth/add_groundtruthrecord_success.html'
