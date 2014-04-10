from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from cartodbsync.models import SyncEntry

from livinglots_organize.models import BaseOrganizer


class Organizer(BaseOrganizer):
    pass


#
# Signals to update CartoDB when an organizer is added or removed from a lot.
#

@receiver(post_save, sender=Organizer,
          dispatch_uid='organize.models.sync_lot_on_create')
def sync_lot_on_create(sender, instance=None, created=False, **kwargs):
    if instance and created:
        SyncEntry.objects.mark_as_pending_update([instance.content_object])


@receiver(post_delete, sender=Organizer,
          dispatch_uid='organize.models.sync_lot_on_delete')
def sync_lot_on_delete(sender, instance=None, **kwargs):
    if instance:
        SyncEntry.objects.mark_as_pending_update([instance.content_object])
