from django.urls import path
from .views import catalog_home

urlpatterns = [
    path('', catalog_home, name='home'),  # Esta URL tendrá el name='home'
]