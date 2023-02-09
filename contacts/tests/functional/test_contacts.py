from django.test import TransactionTestCase
from django.urls import reverse
from contacts.apps import ContactsConfig
from accounts.models import Environment

class EnvironmentsTestCase(TransactionTestCase):
    fixtures = ["users.json", "environments.json"]

    def setUp(self):
        self.environment = Environment.objects.first()
        self.client.force_login(self.environment.site.users.first())

    def testEnvironmentCrud(self):

        

        with self.settings(ALLOWED_HOSTS=("example.com",)):
            with self.settings(CONTACT_STORAGE=ContactsConfig.DEFAULT_SETTINGS['CONTACT_STORAGE']):
                response = self.client.get(
                    reverse("contacts:list", kwargs={'environment': self.environment.slug}), HTTP_HOST="example.com"
                )

                self.assertContains(response, 'No contacts found')
            