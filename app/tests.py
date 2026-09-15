from django.contrib.auth.models import User
from django.test import TestCase

from .models import Movies


class YearFilterTests(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='cinefilo', password='clave')
		Movies.objects.create(
			user=self.user,
			title='Pelicula 2024',
			poster='https://example.com/2024.jpg',
			duration_minutes=100,
			descripcion='Descripcion',
			calificacion=8,
			year=2024,
		)
		Movies.objects.create(
			user=self.user,
			title='Pelicula 2025',
			poster='https://example.com/2025.jpg',
			duration_minutes=120,
			descripcion='Descripcion',
			calificacion=6,
			year=2025,
		)
		self.client.login(username='cinefilo', password='clave')

	def test_index_filters_movies_by_selected_year(self):
		response = self.client.get('/', {'year': 2024})

		self.assertContains(response, 'Pelicula 2024')
		self.assertNotContains(response, 'Pelicula 2025')
		self.assertEqual(response.context['selected_year'], 2024)

	def test_summary_uses_selected_year(self):
		response = self.client.get('/resumen/', {'year': 2025})

		self.assertContains(response, 'Resumen 2025')
		self.assertContains(response, '<strong>1</strong>', html=True)
		self.assertContains(response, '2 horas')
