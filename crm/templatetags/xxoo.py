from django import template
from django.utils.safestring import mark_safe


register = template.Library()

@register.simple_tag
def houyafan(a1,a2):
    return a1+a2