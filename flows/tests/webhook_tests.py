from django.test import TestCase
from flows.models import Webhook


class WebhookTests(TestCase):

	def test_step_run(self):
		webhook = Webhook()