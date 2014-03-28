import re

from django import template
from django.utils.safestring import mark_safe


register = template.Library()


@register.filter
def highlight(text, query):
    """
    Highlight the query within the given text by wrapping the query with a
    span of class "search-highlight". Ignores case.
    """
    css_class = 'search-highlight'
    highlighted, n = re.subn(r'(%s)' % query,
                             r'<span class="%s">\1</span>' % css_class,
                             str(text), flags=re.IGNORECASE)
    return mark_safe(highlighted)
