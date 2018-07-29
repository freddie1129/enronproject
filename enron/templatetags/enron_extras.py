from django import template
register = template.Library()

@register.filter(name='split')
def split(value):
    """Removes all values of arg from the given string"""
    return value.split(',')

