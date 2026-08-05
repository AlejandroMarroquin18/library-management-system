from django.urls import path
from .views import (
    DashboardHomeView,
    # Libros
    LibroListView, LibroCreateView, LibroUpdateView, LibroDeleteView,
    # Autores
    AutorListView, AutorCreateView, AutorUpdateView, AutorDeleteView,
    # Categorías
    CategoriaListView, CategoriaCreateView, CategoriaUpdateView, CategoriaDeleteView,
    # Editoriales
    EditorialListView, EditorialCreateView, EditorialUpdateView, EditorialDeleteView,
    # Préstamos
    LoanListView, LoanCreateView, LoanReturnView,
    # Compras
    CompraListView, CompraDetailView, CompraStatusUpdateView,
    # Usuarios
    UserListView, UserUpdateView, UserToggleActiveView,
)

app_name = 'dashboard'

urlpatterns = [
    # Dashboard Principal
    path('', DashboardHomeView.as_view(), name='home'),
    # Libros
    path('libros/', LibroListView.as_view(), name='libro_list'),
    path('libros/nuevo/', LibroCreateView.as_view(), name='libro_create'),
    path('libros/<int:pk>/editar/', LibroUpdateView.as_view(), name='libro_update'),
    path('libros/<int:pk>/eliminar/', LibroDeleteView.as_view(), name='libro_delete'),
    # Autores
    path('autores/', AutorListView.as_view(), name='autor_list'),
    path('autores/nuevo/', AutorCreateView.as_view(), name='autor_create'),
    path('autores/<int:pk>/editar/', AutorUpdateView.as_view(), name='autor_update'),
    path('autores/<int:pk>/eliminar/', AutorDeleteView.as_view(), name='autor_delete'),
    # Usuarios
    path('usuarios/', UserListView.as_view(), name='usuario_list'),
    path('usuarios/<int:pk>/editar/', UserUpdateView.as_view(), name='usuario_update'),
    path('usuarios/<int:pk>/toggle-activo/', UserToggleActiveView.as_view(), name='usuario_toggle_active'),
    # Compras
    path('compras/', CompraListView.as_view(), name='compra_list'),
    path('compras/<int:pk>/', CompraDetailView.as_view(), name='compra_detail'),
    path('compras/<int:pk>/cambiar-estado/', CompraStatusUpdateView.as_view(), name='compra_status_update'),

    # Categorías
    path('categorias/', CategoriaListView.as_view(), name='categoria_list'),
    path('categorias/nueva/', CategoriaCreateView.as_view(), name='categoria_create'),
    path('categorias/<int:pk>/editar/', CategoriaUpdateView.as_view(), name='categoria_update'),
    path('categorias/<int:pk>/eliminar/', CategoriaDeleteView.as_view(), name='categoria_delete'),

    # Editoriales
    path('editoriales/', EditorialListView.as_view(), name='editorial_list'),
    path('editoriales/nueva/', EditorialCreateView.as_view(), name='editorial_create'),
    path('editoriales/<int:pk>/editar/', EditorialUpdateView.as_view(), name='editorial_update'),
    path('editoriales/<int:pk>/eliminar/', EditorialDeleteView.as_view(), name='editorial_delete'),

    # Préstamos
    path('prestamos/', LoanListView.as_view(), name='prestamo_list'),
    path('prestamos/nuevo/', LoanCreateView.as_view(), name='prestamo_create'),
    path('prestamos/<int:pk>/devolver/', LoanReturnView.as_view(), name='prestamo_return'),
]