from pint import UnitRegistry

from django.conf import settings
from django.contrib.contenttypes import generic
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from cartodbsync.models import SyncEntry
from livinglots import get_stewardproject_model_name
from livinglots_lots.models import (BaseLot, BaseLotGroup, BaseLotLayer,
                                    BaseLotManager)

from organize.models import Organizer


ureg = UnitRegistry()


class LotManager(BaseLotManager):
    pass


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
    steward_projects = generic.GenericRelation(get_stewardproject_model_name())

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
        if self.known_use and self.known_use.visible:
            return 'in_use'

        # Side lots
        try:
            if self.parcel.sidelot_set.count() > 0:
                return 'public_sidelot'
        except Exception:
            pass

        if self.owner and self.owner.owner_type == 'public':
            return 'public'
        if self.owner and self.owner.owner_type == 'private':
            return 'private'

        # Account for lot groups, where the parent likely will not have an
        # owner
        if not self.owner and len(self.lots) > 1:
            owner_types = set(map(lambda l: l.owner.owner_type, self.lots))
            if len(owner_types) == 1:
                return owner_types.pop()
        return ''

    layer = property(_layer)

    def _actively_organizing(self):
        """Actively organizing: has organizers but no steward projects"""
        return self.organizers.exists() and not self.steward_projects.exists()

    actively_organizing = property(_actively_organizing)

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


class LotLayer(BaseLotLayer):

    @classmethod
    def get_layer_filters(cls):
        return {
            'in_use': Q(known_use__visible=True),
            'public': Q(
                Q(known_use=None) | Q(known_use__visible=True),
                (Q(owner__owner_type='public') |
                 Q(lotgroup__lot__lotlayer__name='public')),
            ),
            'private': Q(
                Q(known_use=None) | Q(known_use__visible=True),
                (Q(owner__owner_type='private') |
                 Q(lotgroup__lot__lotlayer__name='private')),
            ),
            'public_sidelot': Q(
                Q(Q(known_use=None) | Q(known_use__visible=True)),
                ~Q(parcel__sidelot=None),
            ),
        }


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
