from django.db import transaction
from django.core.exceptions import ValidationError
from .models import Cart, CartItem, Compra, DetalleCompra
from catalog.models import Libro


class CartService:
    @staticmethod
    def get_or_create_cart(user):
        """Obtiene o crea el carrito activo del usuario."""
        cart, _ = Cart.objects.get_or_create(user=user)
        return cart

    @staticmethod
    def add_book_to_cart(user, libro_id, cantidad=1):
        """Añade un libro al carrito o incrementa su cantidad."""
        libro = Libro.objects.get(id=libro_id)
        
        if libro.stock < cantidad:
            raise ValidationError(f"No hay suficiente stock disponible de '{libro.titulo}'. Stock actual: {libro.stock}")

        cart = CartService.get_or_create_cart(user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, libro=libro)

        if not created:
            nueva_cantidad = cart_item.cantidad + cantidad
            if libro.stock < nueva_cantidad:
                raise ValidationError(f"No puedes agregar más unidades. Stock disponible: {libro.stock}")
            cart_item.cantidad = nueva_cantidad
        else:
            cart_item.cantidad = cantidad

        cart_item.save()
        return cart_item

    @staticmethod
    def remove_item(user, item_id):
        """Elimina un ítem específico del carrito."""
        CartItem.objects.filter(cart__user=user, id=item_id).delete()


class OrderService:
    @staticmethod
    @transaction.atomic
    def checkout(user):
        """
        Convierte los ítems del carrito en una Compra con sus DetalleCompra.
        Usa transaction.atomic para asegurar que si falla el descuento de stock, 
        no se cree la compra (Rollback automático).
        """
        cart = Cart.objects.filter(user=user).prefetch_related('items__libro').first()

        if not cart or not cart.items.exists():
            raise ValidationError("El carrito está vacío.")

        total_compra = 0
        detalles_a_crear = []

        # 1. Validar stock e ir preparando los detalles
        for item in cart.items.all():
            libro = item.libro
            if libro.stock < item.cantidad:
                raise ValidationError(f"Stock insuficiente para '{libro.titulo}'. Disponible: {libro.stock}")

            subtotal = libro.precio_compra * item.cantidad
            total_compra += subtotal

            # Reducir stock del libro
            libro.stock -= item.cantidad
            libro.save()

            # Preparar detalle
            detalles_a_crear.append({
                'libro': libro,
                'cantidad': item.cantidad,
                'precio_unitario': libro.precio_compra,
                'subtotal': subtotal
            })

        # 2. Crear la Compra
        compra = Compra.objects.create(
            usuario=user,
            total=total_compra,
            estado=Compra.Estado.COMPLETADA
        )

        # 3. Crear todos los DetalleCompra
        for d in detalles_a_crear:
            DetalleCompra.objects.create(
                compra=compra,
                libro=d['libro'],
                cantidad=d['cantidad'],
                precio_unitario=d['precio_unitario'],
                subtotal=d['subtotal']
            )

        # 4. Vaciar el carrito
        cart.items.all().delete()

        return compra