from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from users.decorators import admin_required
from .models import Libro, Categoria, Autor, Editorial

# Catálogo con Búsqueda y Filtro
def catalog_home(request):
    libros = Libro.objects.filter(disponible=True).select_related('autor', 'categoria')
    categorias = Categoria.objects.all()

    # --- FASE 5: BÚSQUEDA ---
    search_query = request.GET.get('q', '').strip()
    if search_query:
        # Busca por título del libro o por nombre/apellido del autor
        libros = libros.filter(
            Q(titulo__icontains=search_query) |
            Q(autor__nombre__icontains=search_query) |
            Q(autor__apellido__icontains=search_query) |
            Q(isbn__icontains=search_query)
        )

    # --- FASE 6: FILTRAR ---
    categoria_id = request.GET.get('categoria')
    if categoria_id and categoria_id.isdigit():
        libros = libros.filter(categoria_id=int(categoria_id))

    context = {
        'libros': libros,
        'categorias': categorias,
        'search_query': search_query,
        'categoria_seleccionada': int(categoria_id) if categoria_id and categoria_id.isdigit() else None
    }
    return render(request, 'catalog/catalog_home.html', context)


# VISTA PRIVADA: Solo accesible para el ADMIN
@admin_required
def libro_create(request):
    """
    Vista de administración para añadir libros directamente desde la app.
    Un CUSTOMER que intente entrar aquí recibirá un error HTTP 403.
    """
    if request.method == 'POST':
        # Aquí procesaremos el formulario de creación de libro
        pass
    
    return render(request, 'catalog/libro_form.html')


# 2. Vista de detalle de un Libro
def libro_detail(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    return render(request, 'catalog/libro_detail.html', {'libro': libro})