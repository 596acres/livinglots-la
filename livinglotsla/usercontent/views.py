from django.core.urlresolvers import reverse
from django.views.generic import DetailView

from livinglots_usercontent.notes.models import Note
from livinglots_usercontent.views import AddContentView

from lots.models import Lot
from .forms import FileForm, NoteForm, PhotoForm


class SuccessView(DetailView):
    model = None

    def get_template_names(self):
        return [
            'livinglots/usercontent/add_%s_success.html' % (
                self.model.__name__.lower(),
            )
        ]


class AddFileView(AddContentView):
    content_type_model = Lot
    form_class = FileForm


class AddNoteView(AddContentView):
    content_type_model = Lot
    form_class = NoteForm

    def get_form_valid_message(self):
        return None

    def get_success_url(self):
        return reverse('usercontent:add_note_success', kwargs={
            'pk': self.object.content_object.pk,
            'usercontent_pk': self.object.pk,
        })


class AddNoteSuccessView(SuccessView):
    model = Note
    pk_url_kwarg = 'usercontent_pk'


class AddPhotoView(AddContentView):
    content_type_model = Lot
    form_class = PhotoForm
