from django import template
import random

register = template.Library()

@register.filter(name='sample')
def sample(value, arg):
    try:
        return random.sample(value, int(arg))
    except (ValueError, TypeError, IndexError):
        return value