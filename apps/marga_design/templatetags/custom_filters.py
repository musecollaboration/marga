from django import template

register = template.Library()

@register.filter
def price_filter(value):
    """Разбивает число на тысячные"""
    return f'{value:,d}'.replace(',', ' ')