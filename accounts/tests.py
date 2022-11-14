from django.test import TransactionTestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

class EnvironmentTestCase(TransactionTestCase):
	fixtures = ['user.json']


	def setUp(self):
		pass

	def testEnvironmentCrud(self):
		with self.settings(ALLOWED_HOSTS=('example.com',)):
			self.client.force_login(get_user_model().objects.first())
			
			response = self.client.get(reverse('accounts:environment_list'), HTTP_HOST='example.com')
			self.assertNotContains(response, 'data-bs-target="#delete')

			response = self.client.post(reverse('accounts:environment_create'), 
				{'name': 'test_environment'}, HTTP_HOST='example.com')
			self.assertEqual(response.status_code, 302)
			self.assertEqual(response.headers['location'], reverse('accounts:environment_list'))

			response = self.client.get(reverse('accounts:environment_list'), HTTP_HOST='example.com')
			self.assertContains(response, 'data-bs-target="#delete', count=1)