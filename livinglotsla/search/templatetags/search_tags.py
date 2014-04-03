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


@register.filter
def truncatequery(text, query):
    """
    Truncate the incoming text around the query.
    """
    matches = re.findall(r'(?:\S+\s*){0,3}%s(?:\s*\S+){0,3}' % query, text)
    return mark_safe('...%s...' % '...'.join(matches))
