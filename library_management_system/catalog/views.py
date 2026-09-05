from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView
from django.db.models import Avg, F, Q
from users.decorators import admin_required
from .forms import ReviewForm
from .models import Libro, Categoria, Autor, Editorial, Review


class CatalogHomeView(ListView):
    """
    Vista basada en clase para el catálogo general.
    Mantiene la búsqueda multifiltro (Q), filtrado por categoría y select_related.
    """
    model = Libro
    template_name = 'catalog/catalog_home.html'
    context_object_name = 'libros'
    paginate_by = 12

    def get_queryset(self):
        # Base QuerySet con la optimización JOIN de autor y categoría
        queryset = Libro.objects.filter(disponible=True).select_related('autor', 'categoria')

        # --- BÚSQUEDA ---
        search_query = self.request.GET.get('q', '').strip()
        if search_query:
            queryset = queryset.filter(
                Q(titulo__icontains=search_query) |
                Q(autor__nombre__icontains=search_query) |
                Q(autor__apellido__icontains=search_query) |
                Q(isbn__icontains=search_query)
            )

        # --- FILTRAR POR CATEGORÍA ---
        categoria_id = self.request.GET.get('categoria')
        if categoria_id and categoria_id.isdigit():
            queryset = queryset.filter(categoria_id=int(categoria_id))

        queryset = queryset.annotate(
            promedio_resenas=Avg('resenas__puntuacion', filter=Q(resenas__aprobada=True))
        )
        order = self.request.GET.get('orden', 'titulo')
        if order == 'genero':
            queryset = queryset.order_by('categoria__nombre', 'titulo')
        elif order == 'valoracion':
            queryset = queryset.order_by(F('promedio_resenas').desc(nulls_last=True), 'titulo')
        else:
            order = 'titulo'
            queryset = queryset.order_by('titulo')
        self.order = order
        return queryset

    def get_context_data(self, **kwargs):
        """Pasa las variables adicionales necesarias a la plantilla."""
        context = super().get_context_data(**kwargs)
        
        search_query = self.request.GET.get('q', '').strip()
        categoria_id = self.request.GET.get('categoria')

        context['categorias'] = Categoria.objects.all()
        context['search_query'] = search_query
        context['categoria_seleccionada'] = int(categoria_id) if categoria_id and categoria_id.isdigit() else None
        context['orden_seleccionada'] = getattr(self, 'order', self.request.GET.get('orden', 'titulo'))
        context['ordenes'] = (
            ('titulo', 'Título'),
            ('genero', 'Género'),
            ('valoracion', 'Valoración'),
        )
        
        return context


class LibroDetailView(DetailView):
    """
    Vista de detalle de un libro optimizada.
    Aprovecha select_related para evitar N+1 queries al cargar relaciones.
    """
    model = Libro
    template_name = 'catalog/libro_detail.html'
    context_object_name = 'libro'

    def get_queryset(self):
        return Libro.objects.select_related('autor', 'categoria')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resenas'] = self.object.resenas.filter(aprobada=True).select_related('usuario')
        context['review_form'] = ReviewForm()
        context['promedio_resenas'] = context['resenas'].aggregate(promedio=Avg('puntuacion'))['promedio']
        context['puede_resenar'] = self._user_can_review()
        return context

    def _user_can_review(self):
        if not self.request.user.is_authenticated:
            return False
        from loans.models import Loan
        from sales.models import Compra
        return Compra.objects.filter(
            usuario=self.request.user,
            estado=Compra.Estado.COMPLETADA,
            detalles__libro=self.object,
        ).exists() or Loan.objects.filter(user=self.request.user, book=self.object).exists()


@login_required
@require_POST
def review_create_view(request, book_id):
    libro = get_object_or_404(Libro, pk=book_id)
    from loans.models import Loan
    from sales.models import Compra
    can_review = Compra.objects.filter(
        usuario=request.user,
        estado=Compra.Estado.COMPLETADA,
        detalles__libro=libro,
    ).exists() or Loan.objects.filter(user=request.user, book=libro).exists()
    if not can_review:
        messages.error(request, 'Solo puedes reseñar libros que hayas comprado o solicitado en préstamo.')
        return redirect('libro_detail', pk=libro.pk)
    form = ReviewForm(request.POST)
    if form.is_valid():
        review, created = Review.objects.update_or_create(
            libro=libro,
            usuario=request.user,
            defaults={**form.cleaned_data, 'aprobada': False},
        )
        message = 'Reseña enviada para moderación.' if created else 'Reseña actualizada y enviada para moderación.'
        messages.success(request, message)
    else:
        messages.error(request, 'Revisa la puntuación y el comentario de tu reseña.')
    return redirect('libro_detail', pk=libro.pk)


@login_required
@require_POST
def review_delete_view(request, review_id):
    review = get_object_or_404(Review, pk=review_id, usuario=request.user)
    libro_id = review.libro_id
    review.delete()
    messages.success(request, 'Reseña eliminada.')
    return redirect('libro_detail', pk=libro_id)


@login_required
def review_edit_view(request, review_id):
    review = get_object_or_404(Review, pk=review_id, usuario=request.user)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            review.aprobada = False
            review.save()
            messages.success(request, 'Reseña actualizada y enviada para moderación.')
            return redirect('libro_detail', pk=review.libro_id)
    else:
        form = ReviewForm(instance=review)
    return render(request, 'catalog/review_form.html', {'form': form, 'review': review})


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