from pint import UnitRegistry

from django.conf import settings
from django.contrib.contenttypes import generic
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from cartodbsync.models import SyncEntry
from livinglots_lots.models import BaseLot, BaseLotGroup, BaseLotManager

from organize.models import Organizer
from owners.models import Owner

from .exceptions import ParcelAlreadyInLot


ureg = UnitRegistry()


class LotManager(BaseLotManager):

    def create_lot_for_parcels(self, parcels, **lot_kwargs):
        lots = []

        # Check parcel validity
        for parcel in parcels:
            if parcel.lot_model.count():
                raise ParcelAlreadyInLot()

        # Create lots for each parcel
        for parcel in parcels:
            kwargs = {
                'parcel': parcel,
                'polygon': parcel.geom,
                'centroid': parcel.geom.centroid,
                'address_line1': parcel.street_address,
                'name': parcel.street_address,
                'postal_code': parcel.zip_code,
                'city': parcel.city,
                'state_province': parcel.state or 'CA',
            }
            kwargs.update(**lot_kwargs)

            # Create or get owner for parcels
            if parcel.owner_name:
                (owner, created) = Owner.objects.get_or_create(
                    parcel.owner_name,
                    defaults={
                        'owner_type': parcel.owner_type,
                    }
                )
                kwargs['owner'] = owner

            lot = Lot(**kwargs)
            lot.save()
            lots.append(lot)

        # Multiple lots, create a lot group
        if len(lots) > 1:
            example_lot = lots[0]
            kwargs = {
                'address_line1': example_lot.address_line1,
                'name': example_lot.name,
            }
            kwargs.update(**lot_kwargs)
            lot = LotGroup(**kwargs)
            lot.save()
            lot.update(lots=lots)
        return lot


class LotGroupLotMixin(models.Model):

    group = models.ForeignKey('LotGroup',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_('group'),
    )

    class Meta:
        abstract = True


class LotMixin(models.Model):

    organizers = generic.GenericRelation(Organizer)

    @classmethod
    def get_filter(cls):
        from .filters import LotFilter
        return LotFilter

    def calculate_polygon_area(self):
        try:
            return self.polygon.transform(settings.LOCAL_PROJECTION, clone=True).area
        except Exception:
            return None

    def _area(self):
        if not self.polygon_area:
            self.polygon_area = self.calculate_polygon_area()
            self.save()
        return self.polygon_area

    area = property(_area)

    def _area_acres(self):
        area = self.area * (ureg.feet ** 2)
        return area.to(ureg.acre).magnitude

    area_acres = property(_area_acres)

    def _layer(self):
        if self.known_use:
            return 'in_use'
        elif self.owner and self.owner.owner_type == 'public':
            return 'public'
        elif self.owner and self.owner.owner_type == 'private':
            return 'private'
        return ''

    layer = property(_layer)

    class Meta:
        abstract = True


class Lot(LotMixin, LotGroupLotMixin, BaseLot):

    objects = LotManager()

    parcel = models.ForeignKey(
        'parcels.Parcel',
        related_name='lot_model',
        blank=True,
        null=True
    )

    zoning_district = models.ForeignKey(
        'zoning.ZoningDistrict',
        blank=True,
        null=True,
    )

    class Meta:
        permissions = (
            ('view_preview', 'Can view preview map'),
        )


class LotGroup(BaseLotGroup, Lot):
    objects = models.Manager()


#
# Handle some signals
#


@receiver(post_save, sender=Lot, dispatch_uid='lots.models.sync_on_save')
def sync_on_save(sender, instance=None, created=False, **kwargs):
    if instance and created:
        SyncEntry.objects.mark_as_pending_insert([instance])
    elif instance:
        SyncEntry.objects.mark_as_pending_update([instance])


@receiver(post_delete, sender=Lot, dispatch_uid='lots.models.sync_on_delete')
def sync_on_delete(sender, instance=None, **kwargs):
    if instance:
        SyncEntry.objects.mark_as_pending_delete([instance])
