from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from catalog.models import Autor, Categoria, Libro, Review


class ReviewModerationTests(TestCase):
	@classmethod
	def setUpTestData(cls):
		cls.admin = get_user_model().objects.create_user(
			username='admin-review', password='test-pass-123', role='ADMIN'
		)
		user = get_user_model().objects.create_user(username='reviewer', password='test-pass-123')
		author = Autor.objects.create(nombre='Test', apellido='Author')
		category = Categoria.objects.create(nombre='Test')
		book = Libro.objects.create(
			titulo='Libro de reseña', isbn='9782222222222', precio_compra='10.00',
			precio_alquiler='2.00', stock=1, autor=author, categoria=category,
		)
		cls.review = Review.objects.create(
			libro=book, usuario=user, puntuacion=5, comentario='Excelente', aprobada=False
		)

	def test_approving_review_preserves_five_star_rating(self):
		self.client.login(username='admin-review', password='test-pass-123')

		response = self.client.post(
			reverse('dashboard:review_status_update', args=[self.review.pk]),
			{'estado': 'aprobar'},
		)

		self.assertRedirects(response, reverse('dashboard:review_list'))
		self.review.refresh_from_db()
		self.assertEqual(self.review.puntuacion, 5)
		self.assertTrue(self.review.aprobada)
from django.test import TestCase

# Create your tests here.
