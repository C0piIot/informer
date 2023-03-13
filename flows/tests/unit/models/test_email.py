from unittest.mock import MagicMock, patch

from django.test import TestCase

from accounts.models import Environment
from contacts.apps import ContactsConfig
from contacts.models import Contact
from flows.models import Email, FlowLog, FlowRun


class EmailTestCase(TestCase):
    fixtures = ["users.json", "environments.json", "channels.json"]

    def setUp(self):
        self.environment = Environment.objects.first()
        self.contact = Contact.objects.create(
            key=123,
            name="test",
            environment=self.environment,
            channel_data={
                'emailchannel': {'email': ['test@example.com']}
            }
        )
        self.flow_run = FlowRun(
            environment=self.environment, contact_key=self.contact.key)

    @patch('accounts.models.email_channel.send_mail')
    def test_step_run(self, mock_send_mail):
        with self.settings(CONTACT_STORAGE=ContactsConfig.DEFAULT_SETTINGS['CONTACT_STORAGE']):
            self.flow_run.log = MagicMock()
            email = Email(subject="Subject", html_body="HTML Body",
                          text_body="Text body", site=self.environment.site)
            email.run_next = MagicMock()
            email.step_run(self.flow_run)
            email.run_next.assert_called_with(self.flow_run)
            mock_send_mail.assert_called_once()

    def test_name(self):
        email = Email(subject="Subject", html_body="HTML Body",
                      text_body="Text body", site=self.environment.site)
        self.assertEqual(
            str(email), f'{Email.ICON} Send Email "{email.subject}"')
