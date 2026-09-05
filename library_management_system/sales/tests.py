from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from catalog.models import Autor, Categoria, Libro
from .models import Compra, DetalleCompra


class PurchaseListTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username='buyer', password='test-pass-123')
        author = Autor.objects.create(nombre='Octavia', apellido='Butler')
        category = Categoria.objects.create(nombre='Lecturas')
        cls.book = Libro.objects.create(
            titulo='Libro comprado',
            isbn='9781234567897',
            precio_compra='18.00',
            precio_alquiler='4.00',
            stock=3,
            autor=author,
            categoria=category,
        )
        purchase = Compra.objects.create(
            usuario=cls.user,
            total='18.00',
            estado=Compra.Estado.COMPLETADA,
        )
        DetalleCompra.objects.create(
            compra=purchase,
            libro=cls.book,
            cantidad=1,
            precio_unitario='18.00',
            subtotal='18.00',
        )

    def test_user_can_see_purchased_books(self):
        self.client.login(username='buyer', password='test-pass-123')

        response = self.client.get(reverse('my_purchases'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Libro comprado')
        self.assertEqual(len(response.context['compras']), 1)
