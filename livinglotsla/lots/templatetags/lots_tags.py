from classytags.core import Options
from classytags.arguments import Argument
from classytags.helpers import AsTag
from django import template

from ladata.buildings.models import Building


register = template.Library()


class GetSpecialCategories(AsTag):
    options = Options(
        'for',
        Argument('lot', resolve=True, required=True),
        'as',
        Argument('varname', resolve=False, required=False),
    )

    def get_value(self, context, lot):
        categories = []
        for l in lot.lots:
            if l.parcel.sidelot_set.count() > 0:
                categories.append('Side Yard')
        return categories


class GetVacantReasons(AsTag):
    options = Options(
        'for',
        Argument('lot', resolve=True, required=True),
        'as',
        Argument('varname', resolve=False, required=False),
    )

    def get_value(self, context, lot):
        reasons = []
        for l in lot.lots:
            if l.friendly_owner:
                reasons.append('The owner opted to add it to our map')
            if l.parcel.is_coded_vacant:
                reasons.append('Its use code is vacant according to the LA '
                               'County Assessor')
            if l.parcel.sidelot_set.count() > 0:
                reasons.append("It is in the city's sidelot data")
            if l.parcel.transmissionline_set.count() > 0:
                reasons.append('It is under a transmission line')
            if l.parcel.weedabatement_set.count() > 0:
                reasons.append('It is marked for weed abatement')
            if not Building.objects.filter(geom__overlaps=lot.polygon).exists():
                url = 'http://egis3.lacounty.gov/dataportal/2011/04/28/countywide-building-outlines/'
                reason = """
                    There are no buildings on it according to the
                    <a target="_blank" href="%s">county building outlines</a>
                """ % url
                reasons.append(reason)

            improvement_value = l.parcel.local_roll.improvement_value
            if not improvement_value or improvement_value is 0:
                reasons.append('It has no improvement value according to the '
                               'LA County Assessor')
        return reasons


register.tag(GetSpecialCategories)
register.tag(GetVacantReasons)
