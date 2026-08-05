from django.urls import path
from .views import CatalogHomeView, LibroDetailView, libro_create

urlpatterns = [
    path('', CatalogHomeView.as_view(), name='home'),
    path('libro/<int:pk>/', LibroDetailView.as_view(), name='libro_detail'),
    path('libro/nuevo/', libro_create, name='libro_create'),
]