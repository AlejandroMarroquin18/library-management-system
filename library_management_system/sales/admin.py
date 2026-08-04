from django.contrib import admin
from .models import Cart, CartItem, Compra, DetalleCompra

class DetalleCompraInline(admin.TabularInline):
    model = DetalleCompra
    extra = 0
    readonly_fields = ('libro', 'cantidad', 'precio_unitario', 'subtotal')

@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'fecha', 'estado', 'total')
    list_filter = ('estado', 'fecha')
    search_fields = ('usuario__username', 'id')
    inlines = [DetalleCompraInline]

admin.site.register(Cart)
admin.site.register(CartItem)