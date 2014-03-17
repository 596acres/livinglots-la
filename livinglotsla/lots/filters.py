from hashlib import sha1
from pint import UnitRegistry

from django.db.models import Q

from django.contrib.gis.geos import Polygon
from django.contrib.gis.measure import D

import django_filters

from ladata.communityplanareas.models import CommunityPlanArea
from ladata.councildistricts.models import CouncilDistrict
from ladata.neighborhoodcouncils.models import NeighborhoodCouncil

from .models import Lot


ureg = UnitRegistry()


class BoundingBoxFilter(django_filters.Filter):

    def filter(self, qs, value):
        bbox = Polygon.from_bbox(value.split(','))
        return qs.filter(centroid__within=bbox)


class BoundaryFilter(django_filters.Filter):

    def __init__(self, boundary_model, *args, **kwargs):
        super(BoundaryFilter, self).__init__(*args, **kwargs)
        self.boundary_model = boundary_model

    def filter(self, qs, value):
        if not value:
            return qs
        boundary = self.boundary_model.objects.get(label=value)
        return qs.filter(centroid__within=boundary.geometry)


class LayerFilter(django_filters.Filter):

    def filter(self, qs, value):
        layers = value.split(',')
        layer_filter = Q()

        for layer in layers:
            if layer == 'public':
                layer_filter = layer_filter | Q(
                    Q(known_use=None) | Q(known_use__visible=True),
                    owner__owner_type='public',
                )
            elif layer == 'private':
                layer_filter = layer_filter | Q(
                    Q(known_use=None) | Q(known_use__visible=True),
                    owner__owner_type='private',
                )
        return qs.filter(layer_filter)


class LotGroupParentFilter(django_filters.Filter):

    def filter(self, qs, value):
        if value == 'true':
            qs = qs.filter(group=None)
        return qs


class LotCenterFilter(django_filters.Filter):

    def filter(self, qs, value):
        if not value:
            return qs
        try:
            lot = Lot.objects.get(pk=value)
        except Exception:
            return qs
        return qs.filter(centroid__distance_lte=(lot.centroid, D(mi=.5)))


class OwnerFilter(django_filters.Filter):

    def __init__(self, owner_type=None, **kwargs):
        super(OwnerFilter, self).__init__(**kwargs)
        self.owner_type = owner_type

    def filter(self, qs, value):
        if not value:
            return qs
        owner_pks = value.split(',')
        owner_query = Q(
            Q(known_use=None) | Q(known_use__visible=True),
            owner__owner_type=self.owner_type,
            owner__pk__in=owner_pks,
        )
        other_owners_query = ~Q(owner__owner_type=self.owner_type)
        return qs.filter(owner_query | other_owners_query)


class AcreageMaxFilter(django_filters.Filter):

    def filter(self, qs, value):
        if not value:
            return qs
        max_sq_feet = (float(value) * ureg.acre).to(ureg.feet ** 2)
        return qs.filter(polygon_area__lte=max_sq_feet.magnitude)


class AcreageMinFilter(django_filters.Filter):

    def filter(self, qs, value):
        if not value:
            return qs
        min_sq_feet = (float(value) * ureg.acre).to(ureg.feet ** 2)
        return qs.filter(polygon_area__gte=min_sq_feet.magnitude)


class ProjectFilter(django_filters.Filter):

    def filter(self, qs, value):
        if not value or value == 'include':
            return qs
        has_project_filter = Q(known_use__visible=True)
        if value == 'include':
            return qs
        elif value == 'exclude':
            return qs.filter(~has_project_filter)
        elif value == 'only':
            return qs.filter(has_project_filter)
        return qs


class LotFilter(django_filters.FilterSet):

    bbox = BoundingBoxFilter()
    community_plan_area = BoundaryFilter(CommunityPlanArea)
    council_district = BoundaryFilter(CouncilDistrict)
    layers = LayerFilter()
    lot_center = LotCenterFilter()
    neighborhood_council = BoundaryFilter(NeighborhoodCouncil)
    parents_only = LotGroupParentFilter()
    projects = ProjectFilter()
    public_owners = OwnerFilter(owner_type='public')
    size_max = AcreageMaxFilter()
    size_min = AcreageMinFilter()

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(LotFilter, self).__init__(*args, **kwargs)
        # TODO adjust initial queryset based on user
        self.user = user

    def hashkey(self):
        return sha1(repr(sorted(self.data.items()))).hexdigest()

    class Meta:
        model = Lot
        fields = [
            'address_line1',
            'bbox',
            'council_district',
            'known_use',
            'layers',
            'lot_center',
            'parents_only',
            'projects',
            'public_owners',
            'size_max',
            'size_min',
        ]
