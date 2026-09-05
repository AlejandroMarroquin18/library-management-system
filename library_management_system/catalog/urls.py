from django.urls import path
from .views import CatalogHomeView, LibroDetailView, libro_create, review_create_view, review_delete_view, review_edit_view

urlpatterns = [
    path('', CatalogHomeView.as_view(), name='home'),
    path('libro/<int:pk>/', LibroDetailView.as_view(), name='libro_detail'),
    path('libro/nuevo/', libro_create, name='libro_create'),
    path('libro/<int:book_id>/resena/', review_create_view, name='review_create'),
    path('resena/<int:review_id>/eliminar/', review_delete_view, name='review_delete'),
    path('resena/<int:review_id>/editar/', review_edit_view, name='review_edit'),
]