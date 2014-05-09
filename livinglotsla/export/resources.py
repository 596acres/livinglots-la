from import_export.fields import Field
from import_export.resources import ModelResource

from ladata.communityplanareas.models import CommunityPlanArea
from ladata.councildistricts.models import CouncilDistrict
from ladata.neighborhoodcouncils.models import NeighborhoodCouncil

from lots.models import Lot

# Ensure geojson format is added to tablib
import _geojson


class LotResource(ModelResource):

    address = Field(attribute='parcel__street_address')
    city = Field(attribute='parcel__city')
    community_plan_area = Field()
    council_district = Field()
    latitude = Field(attribute='centroid__y')
    longitude = Field(attribute='centroid__x')
    neighborhood_councils = Field()
    owner = Field(attribute='owner__name')
    owner_type = Field(attribute='owner__owner_type')
    transmission_line_easement = Field()
    weed_abatement = Field()
    zip_code = Field(attribute='parcel__zip_code')
    zone_code = Field(attribute='zoning_district__zone_code')

    class Meta:
        model = Lot
        fields = (
            'pk',
        )

    def get_queryset(self):
        qs = self._meta.model.objects.get_visible()
        qs = qs.select_related('owner', 'parcel', 'zoning_district')
        qs = qs.filter(centroid__isnull=False)
        return qs

    def dehydrate_community_plan_area(self, lot):
        try:
            cpas = CommunityPlanArea.objects.filter(geometry__contains=lot.centroid)
            return ','.join(cpas.values_list('label', flat=True))
        except Exception:
            return ''

    def dehydrate_council_district(self, lot):
        try:
            cds = CouncilDistrict.objects.filter(geometry__contains=lot.centroid)
            return ','.join(cds.values_list('label', flat=True))
        except Exception:
            return ''

    def dehydrate_neighborhood_councils(self, lot):
        try:
            ncs = NeighborhoodCouncil.objects.filter(geometry__contains=lot.centroid)
            return ','.join(ncs.values_list('label', flat=True))
        except Exception:
            return ''

    def dehydrate_transmission_line_easement(self, lot):
        try:
            if lot.parcel.transmissionline_set.count() > 0:
                return 'yes'
        except Exception:
            return 'no'
        return 'no'

    def dehydrate_weed_abatement(self, lot):
        try:
            if lot.parcel.weedabatement_set.count() > 0:
                return 'yes'
        except Exception:
            return 'no'
        return 'no'
