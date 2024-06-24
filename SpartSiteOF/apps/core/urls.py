from django.urls import path
from . import views

urlpatterns = [
    path("", views.CargarIndex),
    path("home", views.CargarIndex, name="home"),
    # productos
    path("Restaurant", views.CargarRestaurant, name="Restaurant"),
    path("Almuerzos", views.CargarAlmuerzos, name="Almuerzos"),
    path("Postres", views.CargarPostres, name="Postres"),
    path("Licores", views.CargarLicores, name="Licores"),
    path("Bebestibles", views.CargarBebestibles, name="Bebestibles"),
    # usuario
    path("profile", views.CargarPerfil, name="profile"),
    # carrito y checkout
    path("Carrito", views.CargarCarrito, name="carrito"),
    path(
        "eliminar-producto/<int:producto_sku>/",
        views.eliminar_producto,
        name="eliminar_producto",
    ),
    path("vaciar-carrito/", views.vaciar_carrito, name="vaciar_carrito"),
    path("agregar-al-carrito/", views.agregar_al_carrito, name="agregar_al_carrito"),
    # mercadopago
    path("process_payment/", views.process_payment, name="process_payment"),
    path("crear_preferencia/", views.crear_preferencia, name="crear_preferencia"),
    path(
        "pago_exitoso/<int:order_id>/", views.cargar_pago_exitoso, name="pago_exitoso"
    ),
    path("pago_fallido/", views.CargarPagofallido, name="pago_exitoso"),
    path("pago_pendiente/", views.CargarPagopendiente, name="pago_exitoso"),
    # productos y opiniones
    path("ver-resenas/<int:producto_sku>/", views.ver_resenas, name="ver_resenas"),
    path(
        "agregar-opinion/<int:producto_sku>",
        views.agregar_opinion,
        name="agregar_opinion",
    ),
    path(
        "detalle-producto/<int:producto_sku>/",
        views.detalle_producto,
        name="detalle_producto",
    ),
    path(
        "agregar-opinion/<int:producto_sku>",
        views.agregar_opinion,
        name="agregar_opinion",
    ),
    # contacto de la pagina
    path("contacto", views.CargarContacto, name="contacto"),
    # envio de corres
    # historial de compras
    path("historial_compras/", views.order_history, name="order_history"),
    path(
        "aplicar_codigo_descuento/",
        views.aplicar_codigo_descuento,
        name="aplicar_codigo_descuento",
    ),
]
