from datetime import datetime
from django import template

register = template.Library()


@register.filter
def ts_to_date(value):
    return datetime.fromtimestamp(int(value))


@register.filter
def wei_to_eth(value):
    return int(value) / 1000000000000000000
