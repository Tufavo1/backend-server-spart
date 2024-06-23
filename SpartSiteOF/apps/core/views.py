from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from .models import *
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .mercadopago import create_payment
from django.views.decorators.http import require_POST


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


def eliminar_producto(request, sku_producto):
    if request.method == "POST":
        carrito = request.session.get("carrito", {})
        if str(sku_producto) in carrito:
            del carrito[str(sku_producto)]
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
    cantidad = 1
    producto = get_object_or_404(Producto, sku=producto_sku)

    if cantidad > 0 and cantidad <= producto.stock:
        carrito = request.session.get("carrito", {})
        if producto_sku in carrito:
            if carrito[producto_sku] + cantidad <= producto.stock:
                carrito[producto_sku] += cantidad
            else:
                return JsonResponse({"error": "out_of_stock"}, status=400)
        else:
            carrito[producto_sku] = cantidad

        request.session["carrito"] = carrito
        request.session.modified = True
        return JsonResponse({"success": "Producto agregado al carrito."})
    else:
        return JsonResponse({"error": "invalid_quantity"}, status=400)


def CargarPerfil(request):
    return render(request, "pages/user/profile.html")


def ver_resenas(request, p_sku):
    producto = Producto.objects.get(sku=p_sku)
    return render(request, "pages/productos/ver_resenas.html", {"producto": producto})


@login_required
def agregar_opinion(request, p_sku):
    if request.method == "POST":
        nombre_usuario = request.user.username
        calificacion = request.POST.get("calificacion")
        comentario = request.POST.get("comentario")

        producto = Producto.objects.get(sku=p_sku)

        opinion = Opinion.objects.create(
            producto=producto,
            nombre_usuario=nombre_usuario,
            calificacion=calificacion,
            comentario=comentario,
        )

        opinion.save()

        return redirect("ver_resenas", p_sku=p_sku)
    else:
        return redirect("inicio")


def detalle_producto(request, p_sku):
    try:
        producto = Producto.objects.get(sku=p_sku)
        return render(request, "ver_resenas.html", {"producto": producto})
    except Producto.DoesNotExist:
        return HttpResponse("El producto solicitado no existe.")


def CargarContacto(request):
    return render(request, "pages/contacto.html")


def checkout_view(request, total):
    return render(request, "pages/pagos/checkout.html", {"total_carrito": total})


@csrf_exempt
def process_payment(request):
    if request.method == "POST":
        payment_response = create_payment(request)

        if payment_response.get("status") == "approved":
            # Actualizar el estado de suscripción del usuario
            user = request.user
            if user.is_authenticated:
                user.is_subscribed = True
                user.save()
                return JsonResponse(
                    {
                        "status": "success",
                        "message": "Payment approved! User subscribed.",
                    }
                )
            else:
                return JsonResponse(
                    {
                        "status": "failure",
                        "message": "Payment approved but user not authenticated.",
                    }
                )
        else:
            return JsonResponse(
                {
                    "status": "failure",
                    "message": payment_response.get("message", "Payment failed"),
                }
            )
    else:
        return JsonResponse({"status": "failure", "message": "Invalid request method."})


def payment_success(request):
    return render(request, "pages/pagos/success.html")


def payment_failure(request):
    return render(request, "pages/pagos/failure.html")
