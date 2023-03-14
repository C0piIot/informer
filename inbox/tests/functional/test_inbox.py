"""Inbox functional testing."""
from django.test import TransactionTestCase
from django.urls import reverse

from accounts.models import Environment
from contacts.apps import ContactsConfig


class InboxTestCase(TransactionTestCase):
    "Inbox list test case"
    fixtures = ["users.json", "environments.json", "channels.json"]

    def setUp(self):
        self.environment = Environment.objects.first()
        self.client.force_login(self.environment.site.users.first())

    def testInbox(self):
        with self.settings(
            ALLOWED_HOSTS=("example.com",),
            CONTACT_STORAGE=ContactsConfig.DEFAULT_SETTINGS["CONTACT_STORAGE"],
        ):
            self.assertContains(
                self.client.get(
                    reverse(
                        "inbox:list", kwargs={
                            "environment": self.environment.slug
                        }
                    ),
                    HTTP_HOST="example.com",
                ),
                "Inbox",
            )
