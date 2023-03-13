from datetime import datetime
from unittest.mock import Mock, call, patch

from django.contrib.sites.models import Site
from django.test import TestCase

from accounts.models import Environment
from stats.storages import BaseStatsStorage, RedisStatsStorage


class RedisStatsStorageTestCase(TestCase):

    def setUp(self):
        self.pipeline = Mock()
        self.pipeline.incr = Mock()
        self.pipeline.expire = Mock()
        self.pipeline.get = Mock()
        self.pipeline.execute = Mock()
        self.environment = Environment(slug="test", site=Site.objects.first())
        RedisStatsStorage.client = Mock()
        RedisStatsStorage.client.pipeline = Mock()
        RedisStatsStorage.client.pipeline.return_value = self.pipeline

    def test_store_events(self):
        with patch('stats.storages.redis_stats_storage.datetime') as mock_datetime:

            mock_datetime.now.return_value = datetime(1983, 6, 25, 1, 15, 30)

            RedisStatsStorage.store_events(
                self.environment, ["event1", "event2"])
            RedisStatsStorage.client.pipeline.assert_called_once()

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
                call(f'count.{site_pk}.test.event1.19830625',
                     31 * 24 * 60 * 60),
                call(f'count.{site_pk}.test.event2.198306250115', 61 * 60),
                call(f'count.{site_pk}.test.event2.1983062501', 25 * 60 * 60),
                call(f'count.{site_pk}.test.event2.19830625',
                     31 * 24 * 60 * 60),
            ])

    def test_read_stas(self):

        with patch('stats.storages.redis_stats_storage.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(1983, 6, 25, 1, 15, 30)

            self.pipeline.execute.return_value = [  # It should return 24 values!
                1, '', '', 5, '', None,
                5, 4, 3, '', '', '',
                1, 1, 1, 1, 1, 1,
                10, 100, 9, '', '', 66
            ]

            response = RedisStatsStorage.read_stats(
                self.environment, 'event', BaseStatsStorage.PERIOD_DAY)

            site_pk = self.environment.site_id

            self.pipeline.get.assert_has_calls([  # 24 calls
                call(f'count.{site_pk}.test.event.1983062401'),
                call(f'count.{site_pk}.test.event.1983062402'),
                call(f'count.{site_pk}.test.event.1983062403'),
                call(f'count.{site_pk}.test.event.1983062404'),
                call(f'count.{site_pk}.test.event.1983062405'),
                call(f'count.{site_pk}.test.event.1983062406'),
                call(f'count.{site_pk}.test.event.1983062407'),
                call(f'count.{site_pk}.test.event.1983062408'),
                call(f'count.{site_pk}.test.event.1983062409'),
                call(f'count.{site_pk}.test.event.1983062410'),
                call(f'count.{site_pk}.test.event.1983062411'),
                call(f'count.{site_pk}.test.event.1983062412'),
                call(f'count.{site_pk}.test.event.1983062413'),
                call(f'count.{site_pk}.test.event.1983062414'),
                call(f'count.{site_pk}.test.event.1983062415'),
                call(f'count.{site_pk}.test.event.1983062416'),
                call(f'count.{site_pk}.test.event.1983062417'),
                call(f'count.{site_pk}.test.event.1983062418'),
                call(f'count.{site_pk}.test.event.1983062419'),
                call(f'count.{site_pk}.test.event.1983062420'),
                call(f'count.{site_pk}.test.event.1983062421'),
                call(f'count.{site_pk}.test.event.1983062422'),
                call(f'count.{site_pk}.test.event.1983062423'),
                call(f'count.{site_pk}.test.event.1983062500'),
                call(f'count.{site_pk}.test.event.1983062501'),
            ])

            response_values = [value for date, value in response]

            self.assertEqual(response_values, [
                1, 0, 0, 5, 0, 0,
                5, 4, 3, 0, 0, 0,
                1, 1, 1, 1, 1, 1,
                10, 100, 9, 0, 0, 66
            ])
