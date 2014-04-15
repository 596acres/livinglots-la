from classytags.core import Options
from classytags.arguments import Argument
from classytags.helpers import AsTag
from django import template


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
            if l.parcel.is_coded_vacant:
                reasons.append('Its use code is vacant according to the LA County '
                            'Assessor')
            if l.parcel.sidelot_set.count() > 0:
                reasons.append("It is in the city's sidelot data")
            if l.parcel.transmissionline_set.count() > 0:
                reasons.append('It is under a transmission line')
            if l.parcel.weedabatement_set.count() > 0:
                reasons.append('It is marked for weed abatement')
        return reasons


register.tag(GetSpecialCategories)
register.tag(GetVacantReasons)
