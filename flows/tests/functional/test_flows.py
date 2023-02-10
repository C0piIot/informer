from django.test import TransactionTestCase
from django.urls import reverse
from accounts.models import Environment
from flows.models import Flow

class EnvironmentsTestCase(TransactionTestCase):
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

            

