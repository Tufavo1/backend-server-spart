from django import template
from babel.numbers import format_currency

register = template.Library()


@register.filter(name="formato_moneda")
def formato_moneda(value):
    formatted = format_currency(value, "CLP", locale="es_CL")
    return formatted.replace(".", ",").replace(",00", "")
