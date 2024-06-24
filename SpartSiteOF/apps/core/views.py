from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.views.decorators.http import require_POST
from .mercadopago import *
import json
from datetime import date


# Create your views here.
def CargarIndex(request):
    productos = Producto.objects.filter(stock__gt="0").order_by("nombre")
    categorias = Categoria.objects.all()
    platillo = Platillo.objects.values("nombre").distinct()

    productos_destacados_por_categoria = []
    for categoria in categorias:
        productos_destacados = Producto.objects.filter(
            categoria=categoria,
            stock__gt=0,
            ventas__gt=0,
        ).order_by("-ventas")[:1]
        productos_destacados_por_categoria.append((categoria, productos_destacados))

    return render(
        request,
        "pages/home.html",
        {
            "productos": productos,
            "cate": categorias,
            "platillo": platillo,
            "productos_destacados_por_categoria": productos_destacados_por_categoria,
        },
    )


def CargarRestaurant(request):
    productos = Producto.objects.filter(stock__gt=0).order_by("nombre")
    categorias = Categoria.objects.all()
    platillo = Platillo.objects.values("nombre").distinct()
    precio_min = float(request.GET.get("precio_min", 0))
    precio_max = float(request.GET.get("precio_max", 1000000))
    productos = productos.filter(precio__gte=precio_min, precio__lte=precio_max)
    platillo_seleccionado = request.GET.getlist("platillo")

    if platillo_seleccionado:
        productos = productos.filter(platillo__nombre__in=platillo_seleccionado)
    buscar = request.GET.get("buscar", "")

    if buscar:
        productos = productos.filter(nombre__icontains=buscar)

    paginator = Paginator(productos, 12)
    page_number = request.GET.get("page")
    page_products = paginator.get_page(page_number)

    return render(
        request,
        "pages/productos/Restaurant.html",
        {
            "prod": page_products,
            "cate": categorias,
            "plat": platillo,
        },
    )


def CargarAlmuerzos(request):
    prodAlm = Producto.objects.filter(stock__gt=0, categoria=2).order_by("nombre")
    categorias = Categoria.objects.all()
    platillo = Platillo.objects.values("nombre").distinct()
    precio_min = float(request.GET.get("precio_min", 0))
    precio_max = float(request.GET.get("precio_max", 1000000))
    productos = prodAlm.filter(precio__gte=precio_min, precio__lte=precio_max)
    platillo_seleccionado = request.GET.getlist("platillo")

    if platillo_seleccionado:
        productos = productos.filter(platillo__nombre__in=platillo_seleccionado)
    buscar = request.GET.get("buscar", "")

    if buscar:
        productos = productos.filter(nombre__icontains=buscar)

    paginator = Paginator(productos, 8)
    page_number = request.GET.get("page")
    page_products = paginator.get_page(page_number)

    return render(
        request,
        "pages/productos/almuerzos.html",
        {"prod": page_products, "cate": categorias, "plat": platillo},
    )


def CargarPostres(request):
    prodPost = Producto.objects.filter(stock__gt=0, categoria=3).order_by("nombre")
    categorias = Categoria.objects.all()
    platillo = Platillo.objects.values("nombre").distinct()
    precio_min = float(request.GET.get("precio_min", 0))
    precio_max = float(request.GET.get("precio_max", 1000000))
    productos = prodPost.filter(precio__gte=precio_min, precio__lte=precio_max)
    platillo_seleccionado = request.GET.getlist("platillo")

    if platillo_seleccionado:
        productos = productos.filter(platillo__nombre__in=platillo_seleccionado)
    buscar = request.GET.get("buscar", "")

    if buscar:
        productos = productos.filter(nombre__icontains=buscar)

    paginator = Paginator(productos, 8)
    page_number = request.GET.get("page")
    page_products = paginator.get_page(page_number)

    return render(
        request,
        "pages/productos/postres.html",
        {"prod": page_products, "cate": categorias, "plat": platillo},
    )


def CargarLicores(request):
    prodLic = Producto.objects.filter(stock__gt=0, categoria=5).order_by("nombre")
    categorias = Categoria.objects.all()
    platillo = Platillo.objects.values("nombre").distinct()
    precio_min = float(request.GET.get("precio_min", 0))
    precio_max = float(request.GET.get("precio_max", 1000000))
    productos = prodLic.filter(precio__gte=precio_min, precio__lte=precio_max)
    platillo_seleccionado = request.GET.getlist("platillo")

    if platillo_seleccionado:
        productos = productos.filter(platillo__nombre__in=platillo_seleccionado)
    buscar = request.GET.get("buscar", "")

    if buscar:
        productos = productos.filter(nombre__icontains=buscar)

    paginator = Paginator(productos, 8)
    page_number = request.GET.get("page")
    page_products = paginator.get_page(page_number)

    return render(
        request,
        "pages/productos/licores.html",
        {"prod": page_products, "cate": categorias, "plat": platillo},
    )


def CargarBebestibles(request):
    prodBeb = Producto.objects.filter(stock__gt=0, categoria=4).order_by("nombre")
    categorias = Categoria.objects.all()
    platillo = Platillo.objects.values("nombre").distinct()
    precio_min = float(request.GET.get("precio_min", 0))
    precio_max = float(request.GET.get("precio_max", 1000000))
    productos = prodBeb.filter(precio__gte=precio_min, precio__lte=precio_max)
    platillo_seleccionado = request.GET.getlist("platillo")

    if platillo_seleccionado:
        productos = productos.filter(platillo__nombre__in=platillo_seleccionado)
    buscar = request.GET.get("buscar", "")

    if buscar:
        productos = productos.filter(nombre__icontains=buscar)

    paginator = Paginator(productos, 8)
    page_number = request.GET.get("page")
    page_products = paginator.get_page(page_number)

    return render(
        request,
        "pages/productos/jugos.html",
        {"prod": page_products, "cate": categorias, "plat": platillo},
    )


def CargarCarrito(request):
    carrito = request.session.get("carrito", {})
    codigos_productos = list(carrito.keys())
    productos = Producto.objects.filter(sku__in=codigos_productos)
    carrito_items = []

    for producto in productos:
        cantidad = carrito[str(producto.sku)]
        carrito_items.append({"producto": producto, "cantidad": cantidad})

    context = {"carrito_items": carrito_items}
    return render(request, "pages/pagos/carrito.html", context)


def eliminar_producto(request, producto_sku):
    if request.method == "POST":
        carrito = request.session.get("carrito", {})
        if str(producto_sku) in carrito:
            del carrito[str(producto_sku)]
            request.session["carrito"] = carrito
        return redirect("carrito")

    return HttpResponse(status=405)


def vaciar_carrito(request):
    if request.method == "POST":
        request.session["carrito"] = {}
        return redirect("carrito")

    return HttpResponse(status=405)


@require_POST
def agregar_al_carrito(request):
    producto_sku = request.POST.get("producto_sku")
    cantidad = int(request.POST.get("cantidad", 1))
    producto = get_object_or_404(Producto, sku=producto_sku)

    if cantidad <= 0:
        messages.error(request, "No hay stock suficiente.")
    elif cantidad > producto.stock:
        messages.error(request, "La cantidad solicitada excede el stock disponible.")
    else:
        carrito = request.session.get("carrito", {})
        if producto_sku in carrito:
            if carrito[producto_sku] + cantidad <= producto.stock:
                carrito[producto_sku] += cantidad
            else:
                messages.error(
                    request, "La cantidad solicitada excede el stock disponible."
                )
        else:
            carrito[producto_sku] = cantidad

        request.session["carrito"] = carrito
        request.session.modified = True
        messages.success(request, "¡Producto agregado al carrito con éxito :)!")

    # Redirigir a la misma página desde donde se hizo la petición
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
def CargarPerfil(request):
    try:
        codigo_descuento = CodigoDescuento.objects.latest("id")
    except CodigoDescuento.DoesNotExist:
        codigo_descuento = None

    context = {"codigo_descuento": codigo_descuento}

    return render(request, "pages/user/profile.html", context)


def aplicar_codigo_descuento(request):
    if request.method == "POST":
        codigo = request.POST.get("codigo")
        try:
            descuento = CodigoDescuento.objects.get(codigo=codigo, activo=True)
            if (
                descuento.fecha_expiracion is None
                or descuento.fecha_expiracion >= date.today()
            ):
                # Verificar si el código ya se ha utilizado
                if "codigos_usados" not in request.session:
                    request.session["codigos_usados"] = []
                if codigo not in request.session["codigos_usados"]:
                    request.session["codigo_descuento"] = codigo
                    request.session["codigos_usados"].append(codigo)
                    messages.success(
                        request, "Código de descuento aplicado correctamente."
                    )
                else:
                    messages.error(
                        request, "Este código de descuento ya ha sido utilizado."
                    )
            else:
                messages.error(request, "Código de descuento expirado.")
        except CodigoDescuento.DoesNotExist:
            messages.error(request, "Código de descuento inválido.")

    return redirect("carrito")


# Historial de productos comprados
@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    context = {"orders": orders}
    return render(request, "pages/user/profile.html", context)


def ver_resenas(request, producto_sku):
    producto = Producto.objects.get(sku=producto_sku)
    # Split the ingredients string
    if producto.ingredientes:
        producto.ingredientes = producto.ingredientes.split(",")
    else:
        producto.ingredientes = []  # Empty list if no ingredients
    return render(request, "pages/productos/ver_resenas.html", {"producto": producto})


@login_required
def agregar_opinion(request, producto_sku):
    if request.method == "POST":
        nombre_usuario = request.user.username
        calificacion = request.POST.get("calificacion")
        comentario = request.POST.get("comentario")

        producto = Producto.objects.get(sku=producto_sku)

        opinion = Opinion.objects.create(
            producto=producto,
            nombre_usuario=nombre_usuario,
            calificacion=calificacion,
            comentario=comentario,
        )

        opinion.save()

        return redirect("ver_resenas", producto_sku=producto_sku)
    else:
        return redirect("inicio")


def detalle_producto(request, producto_sku):
    try:
        producto = Producto.objects.get(sku=producto_sku)
        return render(request, "ver_resenas.html", {"producto": producto})
    except Producto.DoesNotExist:
        return HttpResponse("El producto solicitado no existe.")


def CargarContacto(request):
    return render(request, "pages/contacto.html")


# mercado pago
@csrf_exempt
@login_required
def process_payment(request):
    if request.method == "POST":
        try:
            print("Datos recibidos:", request.body)

            form_data = json.loads(request.body)
            transaction_amount = form_data.get("transaction_amount")
            items = form_data.get("items")

            if items is None or transaction_amount is None:
                return JsonResponse(
                    {"error": "Datos incompletos en la solicitud"}, status=400
                )

            # Crear la orden
            order = Order.objects.create(
                user=request.user, total_amount=transaction_amount
            )

            del request.session["carrito"]
            request.session.modified = True

            # Crear los items de la orden y decrementar el stock
            for item in items:
                producto = get_object_or_404(Producto, sku=item["sku"])
                OrderItem.objects.create(
                    order=order,
                    product=producto,
                    quantity=item["cantidad"],
                    price=item["precio"],
                    image=item.get(
                        "imagen"
                    ),  # Asegúrate de manejar el caso si no hay imagen
                )

                # Decrementar el stock del producto
                try:
                    producto.decrementar_stock(item["cantidad"])
                except ValueError as e:
                    # Manejar el error de stock insuficiente, si es necesario
                    return JsonResponse({"error": str(e)}, status=400)

            # Actualizar estado de la orden a "procesando"
            order.status = "processing"
            order.save()

            # Redirigir a la página de pago exitoso con el ID de la orden
            return JsonResponse({"redirect_url": f"/pago_exitoso/{order.id}/"})

        except json.JSONDecodeError as json_error:
            print("Error JSON:", str(json_error))
            return JsonResponse(
                {"error": "Error al decodificar los datos JSON"}, status=400
            )
        except Exception as e:
            print("Error general:", str(e))
            return JsonResponse({"error": str(e)}, status=500)

    else:
        return JsonResponse({"error": "Método de solicitud no permitido"}, status=405)


@login_required
def crear_preferencia(request):
    if request.method == "POST":
        data = json.loads(request.body)
        transaction_amount = data.get("transaction_amount")
        items = data.get("items")

        # Obtener información del usuario autenticado
        user = request.user
        payer_info = {
            "name": user.first_name,
            "surname": user.last_name,
            "email": user.email,
        }

        preference_items = []
        for item in items:
            preference_items.append(
                {
                    "title": item["nombre"],
                    "quantity": item["cantidad"],
                    "unit_price": item["precio"],
                    "picture_url": item.get(
                        "imagen"
                    ),  # Asegúrate de manejar el caso si no hay imagen
                }
            )

        preference_data = {
            "items": preference_items,
            "payer": payer_info,
            "back_urls": {
                "success": "http://127.0.0.1:8000/pago_exitoso/",
                "failure": "http://127.0.0.1:8000/pago_fallido/",
                "pending": "http://127.0.0.1:8000/pago_pendiente/",
            },
            "auto_return": "approved",
        }

        preference_response = sdk.preference().create(preference_data)
        preference = preference_response["response"]

        return JsonResponse({"preference_id": preference["id"]})


@login_required
def cargar_pago_exitoso(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    context = {"order": order, "items": order.items.all()}
    return render(request, "pages/pagos/exito.html", context)


def CargarPagofallido(request):
    return render(request, "pages/pagos/fallido.html")


def CargarPagopendiente(request):
    return render(request, "pages/pagos/exito.html")
