from django.db import models
from django.conf import settings
from catalog.models import Libro

# 1. MODELOS DE CARRITO (Temporal)
class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='cart'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Carrito de {self.user.username}"

    @property
    def total_price(self):
        return sum(item.subtotal for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'libro')  # Evita duplicar líneas para el mismo libro

    def __str__(self):
        return f"{self.cantidad}x {self.libro.titulo}"

    @property
    def subtotal(self):
        return self.libro.precio_compra * self.cantidad


# 2. MODELOS DE COMPRA (Persistente / Histórico)
class Compra(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE = 'PENDIENTE', 'Pendiente'
        COMPLETADA = 'COMPLETADA', 'Completada'
        CANCELADA = 'CANCELADA', 'Cancelada'

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.PROTECT, 
        related_name='compras'
    )
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=15, choices=Estado.choices, default=Estado.COMPLETADA)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        return f"Compra #{self.id} - {self.usuario.username} (${self.total})"


class DetalleCompra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name='detalles')
    libro = models.ForeignKey(Libro, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.cantidad}x {self.libro.titulo} en Compra #{self.compra.id}"