from django.urls import path
from .views import catalog_home, libro_detail

urlpatterns = [
    path('', catalog_home, name='home'),
    path('libro/<int:pk>/', libro_detail, name='libro_detail'),
]