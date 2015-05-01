from django import template
from django.contrib.contenttypes.models import ContentType

from classytags.arguments import Argument
from classytags.core import Options
from classytags.helpers import AsTag

from livinglots_usercontent.photos.models import Photo

register = template.Library()


class GetRandomPhoto(AsTag):
    options = Options(
        'for',
        Argument('target', required=True, resolve=True),
        'as',
        Argument('varname', required=True, resolve=False),
    )

    def get_value(self, context, target):
        try:
            return Photo.objects.filter(
                content_type=ContentType.objects.get_for_model(target),
                object_id=target.pk,
            ).order_by('?')[0]
        except IndexError:
            return None


register.tag(GetRandomPhoto)
