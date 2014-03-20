from django.conf.urls import patterns, url

from .views import (AddFileView, AddNoteView, AddNoteSuccessView, AddPhotoView,
                    AddPhotoSuccessView)


urlpatterns = patterns('',

    url(r'^photos/add/$',
        AddPhotoView.as_view(),
        name='add_photo'),

    url(r'^photos/(?P<usercontent_pk>\d+)/add/success/$',
        AddPhotoSuccessView.as_view(),
        name='add_photo_success'),

    url(r'^notes/add/$',
        AddNoteView.as_view(),
        name='add_note'),

    url(r'^notes/(?P<usercontent_pk>\d+)/add/success/$',
        AddNoteSuccessView.as_view(),
        name='add_note_success'),

    url(r'^files/add/$',
        AddFileView.as_view(),
        name='add_file'),

)
