from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Autor, Categoria, Libro, Review


class CatalogFeatureTests(TestCase):
	@classmethod
	def setUpTestData(cls):
		cls.user = get_user_model().objects.create_user(username='reader', password='test-pass-123')
		cls.author = Autor.objects.create(nombre='Ada', apellido='Lovelace')
		cls.category = Categoria.objects.create(nombre='Tecnología')
		for index in range(13):
			Libro.objects.create(
				titulo=f'Libro {index}',
				isbn=f'978000000{index:04d}',
				precio_compra='10.00',
				precio_alquiler='2.00',
				stock=2,
				autor=cls.author,
				categoria=cls.category,
			)
		cls.book = Libro.objects.first()

	def test_catalog_is_paginated(self):
		response = self.client.get(reverse('home'))

		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.context['libros']), 12)
		self.assertTrue(response.context['is_paginated'])

	def test_authenticated_user_can_submit_review_for_moderation(self):
		self.client.login(username='reader', password='test-pass-123')

		response = self.client.post(reverse('review_create', args=[self.book.pk]), {
			'puntuacion': 5,
			'comentario': 'Una lectura excelente.',
		})

		self.assertRedirects(response, reverse('libro_detail', args=[self.book.pk]))
		review = Review.objects.get(libro=self.book, usuario=self.user)
		self.assertFalse(review.aprobada)

	def test_public_detail_hides_unapproved_reviews(self):
		Review.objects.create(
			libro=self.book,
			usuario=self.user,
			puntuacion=4,
			comentario='Pendiente',
			aprobada=False,
		)

		response = self.client.get(reverse('libro_detail', args=[self.book.pk]))

		self.assertNotContains(response, 'Pendiente')
from django.test import TestCase

# Create your tests here.
