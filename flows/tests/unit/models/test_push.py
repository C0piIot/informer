from unittest.mock import MagicMock, patch

from django.test import TestCase

from accounts.models import Environment
from contacts.apps import ContactsConfig
from contacts.models import Contact
from flows.models import FlowLog, FlowRun, Push


class PushTestCase(TestCase):
    fixtures = ["users.json", "environments.json", "channels.json"]

    def setUp(self):
        self.environment = Environment.objects.first()
        self.contact = Contact.objects.create(
            key=123,
            name="test",
            environment=self.environment,
            channel_data={"pushchannel": {"fcm_tokens": ["fcm_token"]}},
        )
        self.flow_run = FlowRun(
            environment=self.environment, contact_key=self.contact.key
        )

    @patch("accounts.models.push_channel.firebase_admin")
    @patch("accounts.models.push_channel.messaging.send_multicast")
    def test_step_run(self, mock_firebase_admin, _mock_send_multicast):
        with self.settings(
            CONTACT_STORAGE=ContactsConfig.DEFAULT_SETTINGS["CONTACT_STORAGE"]
        ):
            self.flow_run.log = MagicMock()
            push = Push(
                title="Title", body="Body", url="URL",
                site=self.environment.site)
            push.run_next = MagicMock()
            push.step_run(self.flow_run)
            push.run_next.assert_called_with(self.flow_run)
            mock_firebase_admin.assert_called_once()
            self.flow_run.log.assert_called_with(
                FlowLog.INFO,
                '🔔 Send Push "Title" successful sent to 0 of 0 fcm tokens')

    def test_name(self):
        push = Push(title="Title", body="Body",
                    url="URL", site=self.environment.site)
        self.assertEqual(str(push), f'{Push.ICON} Send Push "{push.title}"')
