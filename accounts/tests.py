from django.test import TransactionTestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

class EnvironmentTestCase(TransactionTestCase):
	fixtures = ['user.json']


	def setUp(self):
		pass

	def testEnvironmentCreate(self):
		self.client.force_login(get_user_model().objects.first())
		self.client.get(reverse('accounts:environment_list'))

