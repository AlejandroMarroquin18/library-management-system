from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from catalog.models import Autor, Categoria, Libro
from .models import Loan


class LoanPaginationTests(TestCase):
	@classmethod
	def setUpTestData(cls):
		cls.user = get_user_model().objects.create_user(username='borrower', password='test-pass-123')
		author = Autor.objects.create(nombre='Grace', apellido='Hopper')
		category = Categoria.objects.create(nombre='Computación')
		book = Libro.objects.create(
			titulo='Libro de pruebas',
			isbn='9781111111111',
			precio_compra='10.00',
			precio_alquiler='2.00',
			stock=20,
			autor=author,
			categoria=category,
		)
		for index in range(11):
			Loan.objects.create(
				user=cls.user,
				book=book,
				due_date=date.today() + timedelta(days=index + 1),
			)

	def test_my_loans_is_paginated(self):
		self.client.login(username='borrower', password='test-pass-123')

		response = self.client.get(reverse('my_loans'))

		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.context['loans']), 10)
		self.assertTrue(response.context['is_paginated'])
from django.test import TestCase

# Create your tests here.
