from django.test import TransactionTestCase
from django.urls import reverse

from accounts.models import Environment
from contacts.apps import ContactsConfig


class ContactsTestCase(TransactionTestCase):
    fixtures = ["users.json", "environments.json", "channels.json"]

    def setUp(self):
        self.environment = Environment.objects.first()
        self.client.force_login(self.environment.site.users.first())

    def testEnvironmentCrud(self):
        with self.settings(
            ALLOWED_HOSTS=("example.com",),
            CONTACT_STORAGE=ContactsConfig.DEFAULT_SETTINGS["CONTACT_STORAGE"],
        ):
            response = self.client.get(
                reverse("contacts:list", kwargs={"environment": self.environment.slug}),
                HTTP_HOST="example.com",
            )

            self.assertContains(response, "No contacts found")

            response = self.client.post(
                reverse(
                    "contacts:contact_create",
                    kwargs={"environment": self.environment.slug},
                ),
                {
                    "name": "example name",
                    "key": 123,
                    "auth_key": "abc",
                    "channels": [1, 2],
                    "contact_data": '{"foo":"bar"}',
                    "channel-1-email": "abc@example.com",
                    "channel-2-fcm_tokens": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                },
                HTTP_HOST="example.com",
                follow=True,
            )

            self.assertRedirects(
                response,
                reverse("contacts:list", kwargs={"environment": self.environment.slug}),
            )

            self.assertNotContains(response, "No contacts found")
            self.assertContains(response, "example name")

            response = self.client.post(
                reverse(
                    "contacts:contact_update",
                    kwargs={"environment": self.environment.slug, "key": 123},
                ),
                {
                    "name": "example name updated",
                    "key": 123,
                    "auth_key": "abc",
                    "channels": [1, 2],
                    "contact_data": '{"foo":"bar"}',
                    "channel-1-email": "abc@example.com",
                    "channel-2-fcm_tokens": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                },
                HTTP_HOST="example.com",
                follow=True,
            )

            self.assertRedirects(
                response,
                reverse("contacts:list", kwargs={"environment": self.environment.slug}),
            )

            self.assertContains(response, "example name updated")

            self.assertRedirects(
                self.client.get(
                    reverse(
                        "contacts:contact_remove",
                        kwargs={"environment": self.environment.slug, "key": 123},
                    ),
                    HTTP_HOST="example.com",
                ),
                reverse("contacts:list", kwargs={"environment": self.environment.slug}),
            )

            response = self.client.post(
                reverse(
                    "contacts:contact_remove",
                    kwargs={"environment": self.environment.slug, "key": 123},
                ),
                HTTP_HOST="example.com",
                follow=True,
            )

            self.assertRedirects(
                response,
                reverse("contacts:list", kwargs={"environment": self.environment.slug}),
            )

            self.assertNotContains(response, "example name updated")
            self.assertContains(response, "Contact was removed successfully")
            self.assertContains(response, "No contacts found")

    def test_viewset(self):
        with self.settings(
            ALLOWED_HOSTS=("example.com",),
            CONTACT_STORAGE=ContactsConfig.DEFAULT_SETTINGS["CONTACT_STORAGE"],
        ):
            response = self.client.post(
                reverse("contact-list", kwargs={"environment": self.environment.slug}),
                {
                    "key": "123",
                    "name": "test",
                    "auth_key": "abc",
                    "contact_data": '{"test" : "test"}',
                    "channel_data": """ 
                        { 
                            \"emailchannel\": { \"email\" : \"test@example.com\"} , 
                            \"pushchannel\" : { \"fcm_tokens\" : [\"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\"] } 
                        }
                    """,
                },
                HTTP_HOST="example.com",
            )
            self.assertEqual(response.status_code, 201)

            response = self.client.post(
                reverse("contact-list", kwargs={"environment": self.environment.slug}),
                {
                    "key": "123",
                    "name": "test",
                    "auth_key": "abc",
                    "contact_data": '{"test" : "test"}',
                    "channel_data": """ 
                        { 
                            \"emailchannel\": { \"email\" : \"test\"} , 
                            \"pushchannel\" : { \"fcm_tokens\" : "non" } 
                        }
                    """,
                },
                HTTP_HOST="example.com",
            )
            self.assertContains(
                response, "Enter a valid email address", status_code=400
            )
            self.assertContains(
                response, "fcm_tokens is expected to be a list", status_code=400
            )
