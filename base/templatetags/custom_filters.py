from django import template

register = template.Library()

@register.filter
def format_views(value):
    if value < 1000:
        return value
    elif value < 1000000:
        return f"{value // 1000}.k"
    else:
        return f"{value // 1000000}.M"
