from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.core.exceptions import ValidationError
from .services import CartService, OrderService
from .models import Compra


# 1. Ver el Carrito de Compras
@login_required
def view_cart(request):
    """
    Obtiene el carrito del usuario. 
    Se asegura que CartService use prefetch_related/select_related para optimizar la plantilla.
    """
    cart = CartService.get_or_create_cart(request.user)
    return render(request, 'sales/cart.html', {'cart': cart})


# 2. Agregar un Libro al Carrito
@login_required
@require_POST
def add_to_cart(request, libro_id):
    """Acción pura de modificación de estado (restringida a POST)."""
    try:
        cantidad = int(request.POST.get('cantidad', 1))
        if cantidad <= 0:
            raise ValidationError("La cantidad debe ser mayor a cero.")
            
        CartService.add_book_to_cart(request.user, libro_id, cantidad)
        messages.success(request, "¡Libro agregado al carrito correctamente!")
    except (ValueError, ValidationError) as e:
        msg = e.message if isinstance(e, ValidationError) else "Cantidad no válida."
        messages.error(request, msg)
        
    return redirect('cart_detail')


# 3. Eliminar un ítem del Carrito
@login_required
@require_POST
def remove_from_cart(request, item_id):
    """Acción pura de modificación de estado (restringida a POST)."""
    try:
        CartService.remove_item(request.user, item_id)
        messages.success(request, "Producto eliminado del carrito.")
    except ValidationError as e:
        messages.error(request, e.message)
        
    return redirect('cart_detail')


# 4. Confirmar la Compra (Checkout)
@login_required
@require_POST
def checkout_view(request):
    """Procesa la transacción del checkout mediante el OrderService."""
    try:
        compra = OrderService.checkout(request.user)
        messages.success(request, f"¡Compra #{compra.id} realizada con éxito!")
        return redirect('order_detail', compra_id=compra.id)
    except ValidationError as e:
        messages.error(request, e.message)
        
    return redirect('cart_detail')


# 5. Ver Detalle de una Compra Realizada
@login_required
def order_detail_view(request, compra_id):
    """
    Muestra el detalle de una compra específica.
    Optimizamos con select_related y prefetch_related para traer la compra,
    sus ítems y los libros relacionados en 1 o 2 queries máximo.
    """
    compra = get_object_or_404(
        Compra.objects.prefetch_related('detalles__libro'), 
        id=compra_id, 
        usuario=request.user
    )
    return render(request, 'sales/order_detail.html', {'compra': compra})