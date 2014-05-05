from django.conf.urls import patterns, url
from django.db.models.signals import post_save

import django_monitor
from django_monitor.util import save_handler

from .models import FriendlyOwner
from .views import AddFriendlyOwnerView, AddFriendlyOwnerSuccessView


urlpatterns = patterns('',

    url(r'^add/$', AddFriendlyOwnerView.as_view(), name='add'),

    url(r'^add/success/$', AddFriendlyOwnerSuccessView.as_view(),
        name='add_success'),

)


django_monitor.nq(FriendlyOwner)


# Disconnect monitor's post-save handler, moderation will be handled in the
# view
post_save.disconnect(save_handler, sender=FriendlyOwner)
