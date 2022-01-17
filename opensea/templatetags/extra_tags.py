from datetime import datetime
from django import template

register = template.Library()


@register.filter
def ts_to_date(value):
    try:
        ttd = datetime.fromtimestamp(int(value))
    except:
        ttd = value
    return ttd


@register.filter
def wei_to_eth(value):
    try:
        wei_to_eth = int(value) / 1000000000000000000
    except:
        wei_to_eth = value
    return wei_to_eth
