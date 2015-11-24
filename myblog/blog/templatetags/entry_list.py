from django import template
from django.template.defaultfilters import stringfilter
register = template.Library()


@register.filter()
@stringfilter
def get_lower(value):
    return "%s %s agao" % (value.lower(), 'fff11f')
