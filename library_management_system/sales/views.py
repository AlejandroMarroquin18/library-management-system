from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from .services import CartService, OrderService
from .models import Compra

# 1. Ver el Carrito de Compras
@login_required
def view_cart(request):
    cart = CartService.get_or_create_cart(request.user)
    return render(request, 'sales/cart.html', {'cart': cart})


# 2. Agregar un Libro al Carrito
@login_required
def add_to_cart(request, libro_id):
    if request.method == 'POST':
        cantidad = int(request.POST.get('cantidad', 1))
        try:
            CartService.add_book_to_cart(request.user, libro_id, cantidad)
            messages.success(request, "¡Libro agregado al carrito correctamente!")
        except ValidationError as e:
            messages.error(request, e.message)
            
    return redirect('cart_detail')


# 3. Eliminar un ítem del Carrito
@login_required
def remove_from_cart(request, item_id):
    if request.method == 'POST':
        CartService.remove_item(request.user, item_id)
        messages.success(request, "Producto eliminado del carrito.")
    return redirect('cart_detail')


# 4. Confirmar la Compra (Checkout)
@login_required
def checkout_view(request):
    if request.method == 'POST':
        try:
            compra = OrderService.checkout(request.user)
            messages.success(request, f"¡Compra #{compra.id} realizada con éxito!")
            return redirect('order_detail', compra_id=compra.id)
        except ValidationError as e:
            messages.error(request, e.message)
            return redirect('cart_detail')

    return redirect('cart_detail')


# 5. Ver Detalle de una Compra Realizada
@login_required
def order_detail_view(request, compra_id):
    compra = get_object_or_404(Compra, id=compra_id, usuario=request.user)
    return render(request, 'sales/order_detail.html', {'compra': compra})