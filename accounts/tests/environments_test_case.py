from django.test import TransactionTestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

class EnvironmentsTestCase(TransactionTestCase):
	fixtures = ['users.json']


	def setUp(self):
		pass

	def testEnvironmentCrud(self):
		with self.settings(ALLOWED_HOSTS=('example.com',)):
			self.client.force_login(get_user_model().objects.first())
			
			self.assertNotContains(
				self.client.get(
					reverse('accounts:environment_list'),
					HTTP_HOST='example.com'
				),
				'data-bs-target="#delete'
			)

			self.assertRedirects(
				self.client.post(
					reverse('accounts:environment_create'), 
					{'name': 'test_environment'},
					HTTP_HOST='example.com'
				),
				reverse('accounts:environment_list')
			)

			self.assertContains(
				self.client.get(
					reverse('accounts:environment_list'),
					HTTP_HOST='example.com'
				), 
				'data-bs-target="#delete',
				count=1
			)
