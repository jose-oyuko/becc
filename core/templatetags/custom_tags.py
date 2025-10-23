from django import template
register = template.Library()

@register.filter
def attr(obj, field_name):
    """Allows accessing object attributes dynamically in templates."""
    return getattr(obj, field_name)
