def total_carrito(request):
    carrito = request.session.get("carrito", {})
    total = 0

    for sku, item in carrito.items():
        # Asegúrate de que item sea un diccionario con la clave 'precio'
        if isinstance(item, dict) and "precio" in item:
            total += int(item.get("precio", 0))

    return {"total_carrito": total}
