from django.db import models, transaction
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from allauth.socialaccount.signals import social_account_added
from django.dispatch import receiver


class Categoria(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, null=False)
    img = models.ImageField(upload_to="imgCategorias", null=True, blank=True)

    def __str__(self):
        txt = "[{0}] {1}"
        return txt.format(self.id, self.nombre)


class Platillo(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, null=False)

    def __str__(self):
        txt = "[{0}] {1}"
        return txt.format(self.id, self.nombre)


class Producto(models.Model):
    sku = models.IntegerField(primary_key=True)
    imagen = models.ImageField(upload_to="imgProductos")
    nombre = models.CharField(max_length=100, null=False)
    descripcion = models.CharField(max_length=100, null=False)
    fecha_ingreso = models.DateField(auto_now_add=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    platillo = models.ForeignKey(Platillo, on_delete=models.CASCADE)
    stock = models.IntegerField(null=False)
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    ventas = models.IntegerField(default=0)
    ingredientes = models.TextField(
        null=True,
        blank=True,
        help_text="Formato: - Ingrediente 1\n- Ingrediente 2, etc.",
    )
    disponible = models.BooleanField(default=True)
    es_suscripcion = models.BooleanField(default=False, editable=False)

    def decrementar_stock(self, cantidad):
        if self.stock >= cantidad:
            self.stock -= cantidad
            if self.stock == 0:
                self.disponible = False
            self.save()
            # Incrementar el contador de ventas
            with transaction.atomic():
                self.ventas += 1
                self.save()
        else:
            raise ValueError("No hay suficiente stock para decrementar.")

    def __str__(self):
        txt = "[{0}] {1} - {2}"
        return txt.format(self.sku, self.platillo, self.nombre)


class CodigoDescuento(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    descuento = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_expiracion = models.DateField(null=True, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.codigo


class Opinion(models.Model):
    producto = models.ForeignKey(
        Producto, on_delete=models.CASCADE, related_name="opiniones"
    )
    nombre_usuario = models.CharField(max_length=100)
    calificacion = models.IntegerField()
    comentario = models.TextField()

    def __str__(self):
        return f"Opinión de {self.nombre_usuario} sobre {self.producto}"


class Boleta(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    transaccion = models.CharField(max_length=100)
    email = models.EmailField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    imagen_producto = models.ImageField(upload_to="productos/")
    fecha_hora = models.DateTimeField(auto_now_add=True)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    is_subscribed = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    def __str__(self):
        return self.email


@receiver(social_account_added)
def handle_social_account_added(sender, request, sociallogin, **kwargs):
    user = sociallogin.user
    if user.email:
        existing_user = CustomUser.objects.filter(email=user.email).first()
        if existing_user and not existing_user.has_usable_password():
            sociallogin.connect(request, existing_user)


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.user.email}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey("Producto", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=0)
    image = models.ImageField(upload_to="imgOrden", null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.image = self.product.imagen
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.product.nombre} - {self.order}"
