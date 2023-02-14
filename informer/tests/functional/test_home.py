from django.test import TestCase
from django.urls import reverse

class HomeTestCase(TestCase):

    def testFlowTest(self):
    
        with self.settings(ALLOWED_HOSTS=("example.com",)):
            self.assertContains(
                self.client.get(
                    reverse("home"),
                    HTTP_HOST="example.com"
                ),
                "Hello there"
            )