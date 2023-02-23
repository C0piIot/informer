from unittest.mock import Mock, call, patch
from datetime import datetime

from django.contrib.sites.models import Site
from django.test import TestCase

from accounts.models import Environment
from stats.storages import RedisStatsStorage

class RedisStatsStorageTestCase(TestCase):

    def setUp(self):
        self.pipeline = Mock()
        self.pipeline.incr = Mock()
        self.pipeline.expire = Mock()
        self.environment = Environment(slug="test", site=Site.objects.first())
        RedisStatsStorage.client = Mock()
        RedisStatsStorage.client.pipeline = Mock()
        RedisStatsStorage.client.pipeline.return_value = self.pipeline

    def test_store_events(self):
        with patch('stats.storages.redis_stats_storage.datetime') as mock_datetime:

            mock_datetime.now.return_value = datetime(1983, 6, 25, 1, 15, 30)

            RedisStatsStorage.store_events(self.environment, ["event1", "event2"])
            RedisStatsStorage.client.pipeline.assert_called_once()
            #self.assertEqual(self.pipeline.incr.call_count, 6)
            site_pk = self.environment.site_id
            self.pipeline.incr.assert_has_calls([
                call(f'count.{site_pk}.test.event1.198306250115'),
                call(f'count.{site_pk}.test.event1.1983062501'),
                call(f'count.{site_pk}.test.event1.19830625'),
                call(f'count.{site_pk}.test.event2.198306250115'),
                call(f'count.{site_pk}.test.event2.1983062501'),
                call(f'count.{site_pk}.test.event2.19830625'),
            ])
            self.pipeline.expire.assert_has_calls([
                call(f'count.{site_pk}.test.event1.198306250115', 61 * 60),
                call(f'count.{site_pk}.test.event1.1983062501', 25 * 60 * 60),
                call(f'count.{site_pk}.test.event1.19830625', 32 * 24 * 60 * 60),
                call(f'count.{site_pk}.test.event2.198306250115', 61 * 60),
                call(f'count.{site_pk}.test.event2.1983062501', 25 * 60 * 60),
                call(f'count.{site_pk}.test.event2.19830625', 32 * 24 * 60 * 60),
            ])

        