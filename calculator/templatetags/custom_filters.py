from django import template

register = template.Library()


@register.filter(name='string_to_int')
def string_to_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None
