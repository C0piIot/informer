from django.test import TestCase
from flows.models import Webhook, FlowRun, FlowLog
from contacts.models import Contact
from unittest.mock import patch, MagicMock
import urllib


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
