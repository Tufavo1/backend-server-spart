from django.template.defaultfilters import floatformat
from .models import Producto
import decimal


def carrito_counter(request):
    carrito = request.session.get("carrito", {})
    carrito_count = sum(carrito.values()) if carrito else 0
    return {"carrito_count": carrito_count}


def subtotal_carrito(request):
    subtotal = decimal.Decimal("0")

    carrito = request.session.get("carrito", {})

    for sku_producto, cantidad in carrito.items():
        producto = Producto.objects.get(sku=sku_producto)
        subtotal += producto.precio * cantidad

    iva = subtotal * decimal.Decimal("0.19")
    total_con_iva = subtotal + iva

    return {
        "subtotal_carrito": floatformat(subtotal, 0),
        "iva": floatformat(iva, 0),
        "total_con_iva": floatformat(total_con_iva, 0),
    }
