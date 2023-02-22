from unittest.mock import MagicMock

from django.contrib.sites.models import Site
from django.test import TestCase

from accounts.models import Environment
from stats.storages import RedisStatsStorage

class RedisStatsStorageTestCase(TestCase):

    def setUp(self):

        self.environment = Environment(slug="test", site=Site.objects.first())
        RedisStatsStorage.client = MagicMock()

    def test_store_events(self):
        RedisStatsStorage.store_events(self.environment, ["event1", "event2"])
        