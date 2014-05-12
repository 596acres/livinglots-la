from django.db import models
from django.db.models import Q

from caching.base import CachingQuerySet, CachingMixin
from feincms.models import Base

from livinglots_pathways.cms import PathwayFeinCMSMixin
from livinglots_pathways.models import BasePathway, BasePathwayManager


class PathwayManager(BasePathwayManager):

    def get_queryset(self):
        return CachingQuerySet(self.model, self._db)

    def get_for_lot(self, lot):
        pathways = super(PathwayManager, self).get_for_lot(lot)

        pathways = pathways.filter(
            Q(minimum_size__isnull=True) | Q(minimum_size__lte=lot.area_acres),
            Q(maximum_size__isnull=True) | Q(maximum_size__gte=lot.area_acres),
        )

        return pathways


class Pathway(CachingMixin, PathwayFeinCMSMixin, BasePathway, Base):
    objects = PathwayManager()

    minimum_size = models.FloatField(
        blank=True,
        null=True,
        help_text='The minimum lot size, in acres',
    )
    maximum_size = models.FloatField(
        blank=True,
        null=True,
        help_text='The maximum lot size, in acres',
    )
