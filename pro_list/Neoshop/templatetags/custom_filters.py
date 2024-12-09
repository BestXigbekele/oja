from django import template

register = template.Library()

@register.filter
def multiply(value1, value2):
    """Multiply two values."""
    try:
        return value1 * value2
    except TypeError:
        return 0