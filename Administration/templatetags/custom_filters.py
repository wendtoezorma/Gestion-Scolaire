# myapp/templatetags/custom_tags.py
from django import template

register = template.Library()

@register.filter
def mul(value1, value2):
    return value1 * value2
