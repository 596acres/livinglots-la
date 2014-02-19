from classytags.core import Options
from classytags.arguments import Argument
from classytags.helpers import AsTag
from django import template


register = template.Library()


class GetVacantReasons(AsTag):
    options = Options(
        'for',
        Argument('lot', resolve=True, required=True),
        'as',
        Argument('varname', resolve=False, required=False),
    )

    def get_value(self, context, lot):
        reasons = []
        if lot.parcel.is_coded_vacant:
            reasons.append('Its use code is vacant according to the LA County '
                           'Assessor')
        return reasons


register.tag(GetVacantReasons)
