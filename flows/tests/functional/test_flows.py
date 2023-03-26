""" Flows functional tests """
from django.contrib.contenttypes.models import ContentType
from django.test import TransactionTestCase
from django.urls import reverse

from accounts.models import Environment
from flows.models import Delay, Flow, Group


class FlowsTestCase(TransactionTestCase):
    """ Flows functional tests """
    fixtures = ["users.json", "environments.json", "channels.json"]

    def setUp(self):
        self.environment = Environment.objects.first()
        self.client.force_login(self.environment.site.users.first())

    def testFlowsCrud(self):
        with self.settings(ALLOWED_HOSTS=("example.com",)):
            self.assertContains(
                self.client.get(
                    reverse(
                        "flows:list",
                        kwargs={"environment": self.environment.slug}),
                    HTTP_HOST="example.com",),
                "No flows found",)

            self.assertRedirects(
                self.client.get(
                    reverse(
                        "flows:create",
                        kwargs={"environment": self.environment.slug}),
                    HTTP_HOST="example.com",),
                reverse(
                    "flows:list",
                    kwargs={"environment": self.environment.slug}),)

            self.assertContains(
                self.client.post(
                    reverse(
                        "flows:create",
                        kwargs={"environment": self.environment.slug}),
                    HTTP_HOST="example.com", follow=True,),
                "Error creating flow",)

            response = self.client.post(
                reverse("flows:create", kwargs={
                        "environment": self.environment.slug}),
                {
                    "name": "example name",
                    "trigger": "example_trigger",
                    "preview_context": '{"foo":"bar"}',
                    "enabled": "",
                },
                HTTP_HOST="example.com",
                follow=True,
            )

            flow = Flow.objects.first()

            self.assertRedirects(
                response,
                reverse(
                    "flows:edit",
                    kwargs={
                        "environment": self.environment.slug,
                        "id": flow.id
                    },
                ),
            )

            response = self.client.post(
                reverse(
                    "flows:edit",
                    kwargs={
                        "environment": self.environment.slug,
                        "id": flow.id
                    },
                ),
                {
                    "name": "example name updated",
                    "trigger": "example_trigger",
                    "preview_context": '{"foo":"bar"}',
                    "enabled": "",
                },
                HTTP_HOST="example.com",
                follow=True,
            )

            self.assertRedirects(
                response,
                reverse(
                    "flows:edit",
                    kwargs={
                        "environment": self.environment.slug,
                        "id": flow.id
                    },
                ),
            )

            self.assertContains(response, "example name updated")

            self.assertRedirects(
                self.client.get(
                    reverse(
                        "flows:remove",
                        kwargs={
                            "environment": self.environment.slug,
                            "id": flow.id
                        },
                    ),
                    HTTP_HOST="example.com",
                    follow=True,
                ),
                reverse("flows:list", kwargs={
                        "environment": self.environment.slug}),
            )

            response = self.client.post(
                reverse(
                    "flows:remove",
                    kwargs={
                        "environment": self.environment.slug,
                        "id": flow.id
                    },
                ),
                HTTP_HOST="example.com",
            )

    def testFlowStepsCrud(self):
        flow = Flow.objects.create(
            name="test flow",
            trigger="test",
            site=self.environment.site,
            user=self.environment.site.users.first(),
        )
        flow.environments.add(self.environment)
        with self.settings(ALLOWED_HOSTS=("example.com",)):
            self.assertContains(
                self.client.get(
                    reverse(
                        "flows:edit",
                        kwargs={"environment": self.environment.slug,
                                "id": flow.id},
                    ),
                    HTTP_HOST="example.com",
                ),
                "This flow has no steps yet.",
            )

            self.client.get(
                reverse(
                    "flows:step_create",
                    kwargs={
                        "environment": self.environment.slug,
                        "id": flow.id,
                        "content_type_id": ContentType.objects.get_for_model(
                            Delay
                        ).pk,
                    },
                ),
                HTTP_HOST="example.com",
                follow=True,
            )

            response = self.client.post(
                reverse(
                    "flows:step_create",
                    kwargs={
                        "environment": self.environment.slug,
                        "id": flow.id,
                        "content_type_id": ContentType.objects.get_for_model(
                            Delay
                        ).pk,
                    },
                ),
                {"time": 30},
                HTTP_HOST="example.com",
                follow=True,
            )

            self.assertRedirects(
                response,
                reverse(
                    "flows:edit",
                    kwargs={
                        "environment": self.environment.slug,
                        "id": flow.id
                    },
                ),
            )

            self.assertContains(response, "Step was created successfully")

            self.assertContains(
                self.client.post(
                    reverse(
                        "flows:step_create",
                        kwargs={
                            "environment": self.environment.slug,
                            "id": flow.id,
                            "content_type_id":
                                ContentType.objects.get_for_model(
                                    Group
                                ).pk,
                        },
                    ),
                    {"key": "test_key", "window": 30},
                    HTTP_HOST="example.com",
                    follow=True,
                ),
                "Step was created successfully",
            )

            first_step = self.environment.flows.first().steps.first()
            self.assertContains(
                self.client.post(
                    reverse(
                        "flows:step_move",
                        kwargs={
                            "environment": self.environment.slug,
                            "id": flow.id,
                            "pk": first_step.pk,
                        },
                    ),
                    HTTP_HOST="example.com",
                    follow=True,
                ),
                "Step moved succesfully",
            )

            last_step = self.environment.flows.first().steps.last()

            self.assertContains(
                self.client.post(
                    reverse(
                        "flows:step_move",
                        kwargs={
                            "environment": self.environment.slug,
                            "id": flow.id,
                            "pk": last_step.pk,
                        },
                    ),
                    {"up": 1},
                    HTTP_HOST="example.com",
                    follow=True,
                ),
                "Step moved succesfully",
            )

            last_step = self.environment.flows.first().steps.last()

            self.assertContains(
                self.client.post(
                    reverse(
                        "flows:step_remove",
                        kwargs={
                            "environment": self.environment.slug,
                            "id": flow.id,
                            "pk": last_step.pk,
                        },
                    ),
                    HTTP_HOST="example.com",
                    follow=True,
                ),
                "Step was removed successfully",
            )

            response = self.client.get(
                reverse(
                    "flows:history",
                    kwargs={
                        "environment": self.environment.slug,
                        "id": flow.id
                    },
                ),
                HTTP_HOST="example.com",
            )

            self.assertContains(response, "accordion-item", count=6)

    def test_preview(self):
        flow = Flow.objects.create(
            name="test flow",
            trigger="test",
            site=self.environment.site,
            user=self.environment.site.users.first(),
            preview_context={"name": "<h1>name</h1>", "color": "red"}
        )
        flow.environments.add(self.environment)
        with self.settings(ALLOWED_HOSTS=("example.com",)):
            response = self.client.post(
                reverse(
                    "flows:preview",
                    kwargs={
                        "environment": self.environment.slug,
                        "id": flow.id
                    },
                ),
                {"mode": "plain", "message": "Hola {{ name }}"},
                HTTP_HOST="example.com"
            )
            self.assertEqual(response.content.decode(), "Hola <h1>name</h1>")

            response = self.client.post(
                reverse(
                    "flows:preview",
                    kwargs={
                        "environment": self.environment.slug,
                        "id": flow.id
                    },
                ),
                {"mode": "html", "message": "Hola {{ name }}"},
                HTTP_HOST="example.com"
            )
            self.assertEqual(
                response.content.decode(),
                "Hola &lt;h1&gt;name&lt;/h1&gt;")

            self.assertContains(self.client.post(
                reverse(
                    "flows:preview",
                    kwargs={
                        "environment": self.environment.slug,
                        "id": flow.id
                    },
                ),
                {
                    "mode": "email",
                    "message": "<style>h1{ color:red }</style><h1>Color is {{ color }}</h1>"
                },
                HTTP_HOST="example.com"
            ),
                '<h1 style="color:red">Color is red</h1>'
            )

            self.assertEqual(self.client.post(
                reverse(
                    "flows:preview",
                    kwargs={
                        "environment": self.environment.slug,
                        "id": flow.id
                    },
                ),
                {
                    "mode": "foo",
                    "message": "{% bad template %}"
                },
                HTTP_HOST="example.com"
            ).status_code, 400)
