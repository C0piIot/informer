from django.test import TransactionTestCase
from unittest.mock import MagicMock
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from contacts.apps import ContactsConfig
from accounts.models import Environment
from contacts.models import Contact
from flows.models import Flow, FlowRun
from flows.executors import DramatiqExecutor


class FlowRunsTestCase(TransactionTestCase):
    fixtures = ["users.json", "environments.json", "channels.json"]

    def setUp(self):
        self.environment = Environment.objects.first()
        self.contact = Contact.objects.create(key=123, name="test", environment=self.environment)
        self.client.force_login(self.environment.site.users.first())


    def testFlowTest(self):
        flow = Flow.objects.create(
            name="test", 
            trigger="test", 
            preview_context={}, 
            site=self.environment.site,
            user=self.environment.site.users.first()
        )
        flow.environments.add(self.environment)
        with self.settings(ALLOWED_HOSTS=("example.com",), CONTACT_STORAGE=ContactsConfig.DEFAULT_SETTINGS['CONTACT_STORAGE']):
            self.assertContains(
                self.client.post(
                    reverse("flows:test", kwargs={'environment': self.environment.slug, 'id': flow.id }),
                    {
                        "contact_key": "9999",
                        "event_payload": "{}"
                    },
                    HTTP_HOST="example.com",
                    follow=True
                ),
                "find contact with key 9999"
            )

            DramatiqExecutor.run = MagicMock()

            response = self.client.post(
                reverse("flows:test", kwargs={'environment': self.environment.slug, 'id': flow.id }),
                {
                    "contact_key": self.contact.key,
                    "event_payload": "{}"
                },
                HTTP_HOST="example.com",
                follow=True
            )

            flow_run = FlowRun.objects.first()
            DramatiqExecutor.run.assert_called_once()
            DramatiqExecutor.run.assert_called_with(flow_run)

            self.assertRedirects(
                response,
                reverse('flows:run', kwargs={'environment': self.environment.slug, 'id': flow.id, 'flow_run_id': flow_run.id })
            )

            self.assertContains(
                response,
                "Flow test engaged"
            )

    def testFlowRunList(self):
        flow = Flow.objects.create(
            name="test", 
            trigger="test", 
            preview_context={}, 
            site=self.environment.site,
            user=self.environment.site.users.first()
        )
        flow.environments.add(self.environment)

        with self.settings(ALLOWED_HOSTS=("example.com",), CONTACT_STORAGE=ContactsConfig.DEFAULT_SETTINGS['CONTACT_STORAGE']):
            self.assertContains(
                self.client.get(
                    reverse("flows:runs", kwargs={'environment': self.environment.slug, 'id': flow.id }),
                    HTTP_HOST="example.com"
                ),
                "No flow runs found"
            )

            flow_run = FlowRun.objects.create(flow_revision=flow, environment=self.environment, contact_key=123)

            self.assertContains(
                self.client.get(
                    reverse("flows:runs", kwargs={'environment': self.environment.slug, 'id': flow.id }),
                    HTTP_HOST="example.com"
                ),
                str(flow_run.pk)
            )

