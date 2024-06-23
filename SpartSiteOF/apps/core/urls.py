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
        "eliminar-producto/<int:sku_producto>/",
        views.eliminar_producto,
        name="eliminar_producto",
    ),
    path("vaciar-carrito/", views.vaciar_carrito, name="vaciar_carrito"),
    path("agregar-al-carrito/", views.agregar_al_carrito, name="agregar_al_carrito"),
    path("checkout/<int:total>/", views.checkout_view, name="checkout"),
    path(
        "process_payment/", views.process_payment, name="process_payment"
    ),  # Nueva ruta
    path("success/", views.payment_success, name="payment_success"),
    path("failure/", views.payment_failure, name="payment_failure"),
    # productos y opiniones
    path("ver-resenas/<int:p_sku>/", views.ver_resenas, name="ver_resenas"),
    path("agregar-opinion/<int:p_sku>", views.agregar_opinion, name="agregar_opinion"),
    path(
        "detalle-producto/<int:p_sku>/", views.detalle_producto, name="detalle_producto"
    ),
    path("agregar-opinion/<int:p_sku>", views.agregar_opinion, name="agregar_opinion"),
    # contacto de la pagina
    path("contacto", views.CargarContacto, name="contacto"),
    # envio de corres
]
