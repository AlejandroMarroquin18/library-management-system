from django.urls import path
from .views import view_cart, add_to_cart, remove_from_cart, checkout_view, order_detail_view

urlpatterns = [
    path('cart/', view_cart, name='cart_detail'),
    path('cart/add/<int:libro_id>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('checkout/', checkout_view, name='checkout'),
    path('order/<int:compra_id>/', order_detail_view, name='order_detail'),
]