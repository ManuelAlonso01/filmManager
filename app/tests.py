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

	def test_index_orders_movies_by_rating(self):
		response = self.client.get('/', {'rating_order': 'desc'})
		self.assertEqual(
			[movie.title for movie in response.context['movies']],
			['Pelicula 2024', 'Pelicula 2025'],
		)

		response = self.client.get('/', {'rating_order': 'asc'})
		self.assertEqual(
			[movie.title for movie in response.context['movies']],
			['Pelicula 2025', 'Pelicula 2024'],
		)

	def test_index_combines_year_rating_and_favorite_filters(self):
		Movies.objects.create(
			user=self.user,
			title='Favorita 2025',
			poster='https://example.com/favorita.jpg',
			duration_minutes=90,
			descripcion='Descripcion',
			calificacion=9,
			year=2025,
			favorite=True,
		)

		response = self.client.get('/', {
			'year': 2025,
			'rating_order': 'desc',
			'favorites': 'on',
		})

		self.assertEqual(
			[movie.title for movie in response.context['movies']],
			['Favorita 2025'],
		)
		self.assertTrue(response.context['favorites_only'])

	def test_summary_uses_selected_year(self):
		response = self.client.get('/resumen/', {'year': 2025})

		self.assertContains(response, 'Resumen 2025')
		self.assertContains(response, '<strong>1</strong>', html=True)
		self.assertContains(response, '2 horas')

	def test_summary_includes_pdf_export_branding(self):
		response = self.client.get('/resumen/')

		self.assertContains(response, 'Descargar PDF')
		self.assertContains(response, 'FilmManager')
		self.assertContains(response, 'summary-brand-mark')

	def test_summary_pdf_download_uses_username_in_filename(self):
		response = self.client.get('/resumen/pdf/')

		self.assertEqual(response['Content-Type'], 'application/pdf')
		self.assertIn('Estadisticas de la coleccion de cinefilo.pdf', response['Content-Disposition'])
		self.assertTrue(response.content.startswith(b'%PDF-1.4'))
		self.assertIn(b'46494C4D4D414E41474552', response.content)

	def test_summary_pdf_download_respects_selected_year(self):
		response = self.client.get('/resumen/pdf/', {'year': 2025})

		self.assertEqual(response['Content-Type'], 'application/pdf')
		self.assertIn(b'32303235', response.content)
		self.assertIn(b'3220686F726173', response.content)
		self.assertNotIn(b'3320686F726173', response.content)
