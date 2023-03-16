from django.test import TransactionTestCase
from django.urls import reverse

from accounts.models import Environment


class StatsTestCase(TransactionTestCase):
    fixtures = ["users.json", "environments.json", "channels.json"]

    def setUp(self):
        self.environment = Environment.objects.first()
        self.client.force_login(self.environment.site.users.first())

    def testDashboard(self):
        with self.settings(ALLOWED_HOSTS=("example.com",)):
            self.assertContains(
                self.client.get(
                    reverse(
                        "stats:dashboard",
                        kwargs={"environment": self.environment.slug}),
                    HTTP_HOST="example.com",),
                "Dashboard",)
