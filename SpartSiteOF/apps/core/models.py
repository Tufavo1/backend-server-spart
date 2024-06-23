from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from allauth.socialaccount.signals import social_account_added
from allauth.socialaccount.models import SocialAccount
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

    def __str__(self):
        txt = "[{0}] {1} - {2}"
        return txt.format(self.sku, self.platillo, self.nombre)


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
