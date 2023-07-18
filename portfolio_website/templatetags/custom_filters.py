from django import template

register = template.Library()


@register.filter
def custom_range(start, end):
    return range(start, end)
