import urllib
from unittest.mock import MagicMock, patch
from urllib.parse import urlparse

from django.test import TestCase

from contacts.models import Contact
from flows.models import FlowLog, FlowRun, Webhook


class WebhookTestCase(TestCase):
    def test_step_run(self):
        flow_run = FlowRun()
        flow_run._contact = Contact(key="test-key", name="test-name")
        flow_run.log = MagicMock()

        webhook = Webhook(
            url="http://example.com",
            method="POST",
            contenttype="application/json",
            body='{ "a":"{{ testvar }}"}',
        )
        webhook.run_next = MagicMock()

        response = MagicMock(name="response")
        response.__enter__.return_value.getcode.return_value = 200

        with patch.object(
            urllib.request, "urlopen", return_value=response
        ) as mock_urlopen:
            webhook.step_run(flow_run)

        mock_urlopen.assert_called_once()
        webhook.run_next.assert_called_with(flow_run)
        flow_run.log.assert_called_with(
            FlowLog.INFO, "Webhook POST http://example.com response: 200"
        )

    def test_name(self):
        webhook = Webhook(
            url="http://example.com",
            method="POST",
            contenttype="application/json",
            body='{ "a":"{{ testvar }}"}',
        )
        self.assertEqual(str(webhook), f'{Webhook.ICON} Webhook {webhook.method} {urlparse(webhook.url).netloc}')