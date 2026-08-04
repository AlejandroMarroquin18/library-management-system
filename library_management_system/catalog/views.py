from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def catalog_home(request):
    # lista vacia de libros por ahora, luego se llenará con los libros de la base de datos
    context = {
        'books': []
    }
    return render(request, 'catalog/catalog_home.html', context)