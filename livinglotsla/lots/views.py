import geojson
import json
from pint import UnitRegistry
from random import shuffle

from django.db.models import Count, Sum
from django.http import Http404

from caching.base import cached

from inplace.views import GeoJSONListView
from livinglots_genericviews.views import JSONResponseView
from livinglots_lots.views import (BaseCreateLotView, FilteredLotsMixin,
                                   LotsCountView)
from livinglots_lots.views import LotsCSV as BaseLotsCSV
from livinglots_lots.views import LotsKML as BaseLotsKML
from livinglots_lots.views import LotsGeoJSON as BaseLotsGeoJSON

from ladata.parcels.models import Parcel

from .models import Lot


ureg = UnitRegistry()


class LotDetailJSON(JSONResponseView):

    def get_context_data(self, **kwargs):
        try:
            lot = Lot.objects.get(pk=kwargs['pk'])
        except Exception:
            raise Http404
        return self.get_properties(lot)

    def get_ain(self, lot):
        try:
            if lot.parcel:
                return lot.parcel.ain
            return ', '.join(map(lambda l: l.parcel.ain, lot.lots))
        except Exception:
            return None

    def get_owner_name(self, lot):
        try:
            return str(lot.owner.name) or 'unknown',
        except Exception:
            try:
                return ', '.join(map(lambda l: l.owner.name, lot.lots))
            except Exception:
                return None

    def get_owner_type(self, lot):
        try:
            return str(lot.owner.owner_type) or 'unknown',
        except Exception:
            try:
                return ', '.join(set(map(lambda l: l.owner.owner_type, lot.lots)))
            except Exception:
                return None

    def get_properties(self, lot):
        properties = {
            'address_line1': lot.address_line1,
            'ain': self.get_ain(lot),
            'centroid': [lot.centroid.x, lot.centroid.y],
            'has_organizers': lot.organizers.count() > 0,
            'layer': lot.layer,
            'number_of_lots': lot.number_of_lots,
            'number_of_lots_plural': lot.number_of_lots > 1,
            'organizers_count': lot.organizers.count(),
            'organizers_count_plural': lot.organizers.count() > 1,
            'owner': {
                'name': self.get_owner_name(lot),
                'type': self.get_owner_type(lot),
            },
            'pk': lot.pk,
            'size': round(lot.area_acres, 2),
        }
        try:
            properties['zone_class'] = lot.zoning_district.zone_class
        except Exception:
            pass
        return properties


class LotGeoJSONMixin(object):

    def get_acres(self, lot):
        acres = getattr(lot, 'area_acres', None)
        if not acres:
            return 'unknown'
        return round(acres, 2)

    def get_properties(self, lot):
        return {
            # XXX expensive!
            'layer': lot.layer,
        }

    def get_geometry(self, lot):
        try:
            lot_geojson = lot.geojson
        except Exception:
            if lot.polygon:
                lot_geojson = lot.polygon.geojson
            else:
                lot_geojson = lot.centroid.geojson
        return json.loads(lot_geojson)

    def get_feature(self, lot):
        return geojson.Feature(
            lot.pk,
            geometry=self.get_geometry(lot),
            properties=self.get_properties(lot),
        )


class LotsGeoJSONCentroid(LotGeoJSONMixin, FilteredLotsMixin, GeoJSONListView):

    def get_queryset(self):
        return self.get_lots().qs.filter(centroid__isnull=False).geojson(
            field_name='centroid',
            precision=8,
        ).select_related(
            'known_use',
            'lotgroup',
            'owner__owner_type'
        ).annotate(organizers__count=Count('organizers'))

    def get_features(self):
        filterset = self.get_lots()
        key = '%s:%s' % (self.__class__.__name__, filterset.hashkey())

        def _get_value():
            features = super(LotsGeoJSONCentroid, self).get_features()
            shuffle(features)
            return features
        return cached(_get_value, key, 60 * 15)


class LotsGeoJSONPolygon(LotGeoJSONMixin, FilteredLotsMixin, GeoJSONListView):

    def get_properties(self, lot):
        properties = super(LotsGeoJSONPolygon, self).get_properties(lot)
        properties['centroid'] = (
            round(lot.centroid.x, 4),
            round(lot.centroid.y, 4)
        )
        properties['friendly_owner'] = lot.friendly_owner
        # XXX expensive!
        properties['organizing'] = lot.actively_organizing
        return properties

    def get_queryset(self):
        # TODO would be nice to get sidelots and organizers more efficiently
        return self.get_lots().qs.filter(polygon__isnull=False).geojson(
            field_name='polygon',
            precision=8,
        ).select_related(
            'known_use',
            'lotgroup',
            'owner__owner_type',
            'parcel',
        ).annotate(organizers__count=Count('organizers'))

    def get_features(self):
        filterset = self.get_lots()
        key = '%s:%s' % (self.__class__.__name__, filterset.hashkey())

        def _get_value():
            return super(LotsGeoJSONPolygon, self).get_features()
        return cached(_get_value, key, 60 * 15)


class LotsCountViewWithAcres(LotsCountView):

    def get_acres(self, lots):
        try:
            sf = lots.distinct().aggregate(Sum('polygon_area'))['polygon_area__sum']
            acres = (sf * ureg.feet ** 2).to(ureg.acre).magnitude
            return int(round(acres, 0))
        except Exception:
            return 0

    def get_context_data(self, **kwargs):
        lots = self.get_lots().qs
        no_known_use = lots.filter(known_use__isnull=True)
        in_use = lots.filter(known_use__isnull=False, known_use__visible=True)

        context = {
            'lots-acres': self.get_acres(lots.distinct()),
            'lots-count': lots.distinct().count(),
            'friendly-owner-count': lots.filter(owner_opt_in=True).filter(steward_projects=None).distinct().count(),
            'organized-count': lots.exclude(organizers=None).filter(steward_projects=None).distinct().count(),
            'private-lots-count': lots.filter(lotlayer__name='private').distinct().count(),
            'private-taxdefault-count': 0,
            'public-lots-count': lots.filter(lotlayer__name='public').distinct().count(),
            'public-sidelot-count': lots.filter(lotlayer__name='public_sidelot').distinct().count(),
            'public-remnant-count': 0,
            'no-known-use-count': no_known_use.distinct().count(),
            'in-use-count': in_use.distinct().count(),
        }
        return context


class LotsCSV(BaseLotsCSV):

    def get_sitename(self):
        return 'LA Open Acres'


class LotsKML(BaseLotsKML):

    def get_sitename(self):
        return 'LA Open Acres'


class LotsGeoJSON(BaseLotsGeoJSON):

    def get_sitename(self):
        return 'LA Open Acres'


class CreateLotView(BaseCreateLotView):

    def get_parcels(self, pks):
        return Parcel.objects.filter(pk__in=pks)
