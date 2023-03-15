from unittest.mock import MagicMock

from django.test import TransactionTestCase
from django.urls import reverse

from accounts.models import Environment
from contacts.apps import ContactsConfig
from contacts.models import Contact
from flows.executors import DramatiqExecutor
from flows.models import Flow, FlowRun


class FlowRunsTestCase(TransactionTestCase):
    fixtures = ["users.json", "environments.json", "channels.json"]

    def setUp(self):
        self.environment = Environment.objects.first()
        self.contact = Contact.objects.create(
            key=123, name="test", environment=self.environment
        )
        self.client.force_login(self.environment.site.users.first())
        self.flow = Flow.objects.create(
            name="test",
            trigger="test",
            preview_context={},
            site=self.environment.site,
            user=self.environment.site.users.first(),
        )
        self.flow.environments.add(self.environment)

    def testFlowTest(self):
        with self.settings(
            ALLOWED_HOSTS=("example.com",),
            CONTACT_STORAGE=ContactsConfig.DEFAULT_SETTINGS["CONTACT_STORAGE"],
        ):
            self.assertContains(
                self.client.post(
                    reverse(
                        "flows:test",
                        kwargs={
                            "environment": self.environment.slug,
                            "id": self.flow.id,
                        },
                    ),
                    {"contact_key": "9999", "event_payload": "{}"},
                    HTTP_HOST="example.com",
                    follow=True,
                ),
                "find contact with key 9999",
            )

            DramatiqExecutor.run = MagicMock()

            response = self.client.post(
                reverse(
                    "flows:test",
                    kwargs={"environment": self.environment.slug,
                            "id": self.flow.id},
                ),
                {"contact_key": self.contact.key, "event_payload": "{}"},
                HTTP_HOST="example.com",
                follow=True,
            )

            flow_run = FlowRun.objects.first()
            DramatiqExecutor.run.assert_called_once()
            DramatiqExecutor.run.assert_called_with(flow_run)

            self.assertRedirects(
                response,
                reverse(
                    "flows:run",
                    kwargs={
                        "environment": self.environment.slug,
                        "id": self.flow.id,
                        "flow_run_id": flow_run.id,
                    },
                ),
            )

            self.assertContains(response, "Flow test engaged")

    def testFlowRunList(self):
        with self.settings(
            ALLOWED_HOSTS=("example.com",),
            CONTACT_STORAGE=ContactsConfig.DEFAULT_SETTINGS["CONTACT_STORAGE"],
        ):
            self.assertContains(
                self.client.get(
                    reverse(
                        "flows:runs",
                        kwargs={
                            "environment": self.environment.slug,
                            "id": self.flow.id,
                        },
                    ),
                    HTTP_HOST="example.com",
                ),
                "No flow runs found",
            )

            flow_run = FlowRun.objects.create(
                flow_revision=self.flow, environment=self.environment, contact_key=123
            )

            self.assertContains(
                self.client.get(
                    reverse(
                        "flows:runs",
                        kwargs={
                            "environment": self.environment.slug,
                            "id": self.flow.id,
                        },
                    ),
                    HTTP_HOST="example.com",
                ),
                str(flow_run.pk),
            )

    def test_viewset(self):
        with self.settings(
            ALLOWED_HOSTS=("example.com",),
            CONTACT_STORAGE=ContactsConfig.DEFAULT_SETTINGS["CONTACT_STORAGE"],
        ):
            response = self.client.post(
                reverse("flowrun-list",
                        kwargs={"environment": self.environment.slug}),
                {
                    "event": self.flow.trigger,
                    "contact_key": "this-key-does-not-exist",
                    "event_payload": "{}",
                },
                HTTP_HOST="example.com",
            )
            self.assertEqual(response.status_code, 400)

            response = self.client.post(
                reverse("flowrun-list",
                        kwargs={"environment": self.environment.slug}),
                {
                    "event": self.flow.trigger,
                    "contact_key": self.contact.key,
                    "event_payload": "{}",
                },
                HTTP_HOST="example.com",
            )
            self.assertEqual(response.status_code, 201)
