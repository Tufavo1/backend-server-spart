from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from .models import *
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .mercadopago import create_payment
from django.views.decorators.http import require_POST
from django.contrib import messages


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
    productos = Producto.objects.filter(stock__gt="0").order_by("nombre")
    categorias = Categoria.objects.all()
    platillo = Platillo.objects.values("nombre").distinct()
    paginator = Paginator(productos, 9)
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
    prodAlm = Producto.objects.filter(stock__gt="0", platillo="2").order_by("nombre")
    platillo = Platillo.objects.all()
    categorias = Producto.objects.values("platillo").distinct()
    paginator = Paginator(prodAlm, 6)
    page_number = request.GET.get("page")
    page_products = paginator.get_page(page_number)

    return render(
        request,
        "pages/productos/almuerzos.html",
        {"prod": page_products, "cate": categorias, "plat": platillo},
    )


def CargarPostres(request):
    prodPost = Producto.objects.filter(stock__gt="0", platillo="3").order_by("nombre")
    categorias = Categoria.objects.all()
    platillo = Producto.objects.values("platillo").distinct()
    paginator = Paginator(prodPost, 6)
    page_number = request.GET.get("page")
    page_products = paginator.get_page(page_number)

    return render(
        request,
        "pages/productos/postres.html",
        {"prod": page_products, "cate": categorias, "plat": platillo},
    )


def CargarLicores(request):
    prodLic = Producto.objects.filter(stock__gt="0", platillo="2").order_by("nombre")
    categorias = Categoria.objects.all()
    platillo = Producto.objects.values("platillo").distinct()
    paginator = Paginator(prodLic, 6)
    page_number = request.GET.get("page")
    page_products = paginator.get_page(page_number)

    return render(
        request,
        "pages/productos/licores.html",
        {"prod": page_products, "cate": categorias, "plat": platillo},
    )


def CargarBebestibles(request):
    prodBeb = Producto.objects.filter(stock__gt="0", platillo="1").order_by("nombre")
    categorias = Categoria.objects.all()
    platillo = Producto.objects.values("platillo").distinct()
    paginator = Paginator(prodBeb, 6)
    page_number = request.GET.get("page")
    page_products = paginator.get_page(page_number)

    return render(
        request,
        "pages/productos/jugos.html",
        {"prod": page_products, "cate": categorias, "plat": platillo},
    )


def CargarCarrito(request):
    return render(request, "pages/pagos/carrito.html")


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
    else:
        return JsonResponse({"error": "invalid_quantity"}, status=400)

    return JsonResponse({"success": "Producto agregado al carrito."})


def CargarPerfil(request):
    return render(request, "account/profile.html")


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
