from django.test import TransactionTestCase
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from accounts.models import Environment
from flows.models import Flow, Delay, Email, Group, Push, Webhook

class FlowsTestCase(TransactionTestCase):
    fixtures = ["users.json", "environments.json", "channels.json", "email_channels.json", "push_channels.json"]

    def setUp(self):
        self.environment = Environment.objects.first()
        self.client.force_login(self.environment.site.users.first())


    def testFlowsCrud(self):
        with self.settings(ALLOWED_HOSTS=("example.com",)):

            response = self.client.get(
                reverse("flows:list", kwargs={'environment': self.environment.slug}), HTTP_HOST="example.com"
            )

            self.assertContains(response, 'No flows found')


            response = self.client.post(
                reverse("flows:create", kwargs={'environment': self.environment.slug}),
                {
                    "name": "example name",
                    "trigger": "example_trigger",
                    "preview_context" : "{\"foo\":\"bar\"}",
                    "enabled" : "",
            
                },
                HTTP_HOST="example.com",
                follow=True
            )

            flow = Flow.objects.first()

            self.assertRedirects(
                response,
                reverse("flows:edit", kwargs={'environment': self.environment.slug, 'id': flow.id }),
            )

            self.assertRedirects(
                self.client.get(
                    reverse("flows:remove", kwargs={'environment': self.environment.slug,  'id': flow.id}),
                    HTTP_HOST="example.com",
                    follow=True
                ),
                reverse("flows:list", kwargs={'environment': self.environment.slug})
            )

            response = self.client.post(
                reverse("flows:remove", kwargs={'environment': self.environment.slug,  'id': flow.id}),
                HTTP_HOST="example.com",
    
            )
            

    def testFlowStepsCrud(self):

        flow = Flow.objects.create(name="test flow", trigger="test", site=self.environment.site, user=self.environment.site.users.first())
        flow.environments.add(self.environment)
        with self.settings(ALLOWED_HOSTS=("example.com",)):
            self.assertContains(
                self.client.get(
                    reverse("flows:edit", kwargs={'environment': self.environment.slug,  'id': flow.id}),
                    HTTP_HOST="example.com"
                ),
                "This flow has no steps yet."
            )

            response = self.client.post(
                reverse(
                    "flows:step_create", 
                    kwargs={'environment': self.environment.slug,  'id': flow.id, 'content_type_id': ContentType.objects.get_for_model(Delay).pk },

                ),
                { "time": 30 },
                HTTP_HOST="example.com",
                follow=True
            )

            self.assertRedirects(
                response,
                reverse("flows:edit", kwargs={'environment': self.environment.slug, 'id': flow.id }),
            )

            self.assertContains(
                response,
                "Step was created successfully"
            )
