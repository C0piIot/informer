from datetime import datetime

import environ
import redis
from django.utils.module_loading import import_string
from redis.exceptions import ResponseError

from .base_series_storage import BaseSeriesStorage

env = environ.Env()


class RedisStatsStorage(BaseSeriesStorage):
    ONE_MINUTE_MSECS = 60000
    COMPACT_SUFFIX = {
        BaseSeriesStorage.PERIOD_HOUR: "_SUM_60000_60000",
        BaseSeriesStorage.PERIOD_DAY: "_SUM_1800000_1800000",
        BaseSeriesStorage.PERIOD_MONTH: "_SUM_86400000_86400000",
    }

    client = None

    @classmethod
    def get_connection(cls):
        if not cls.client:
            cls.client = redis.from_url(env.str("STATS_REDIS_URL"))
        return cls.client

    @classmethod
    def store_event(cls, environment, event):
        cls.get_connection().ts().add(
            f"ts.{environment.site.pk}.{environment.slug}.{event}",
            "*",
            1,
            retention_msecs=cls.ONE_MINUTE_MSECS,
        )

    @classmethod
    def read_series(cls, environment, event, period):
        try:
            return [
                (datetime.fromtimestamp(timestamp / 1000), count)
                for timestamp, count in cls.get_connection()
                .ts()
                .range(
                    f"ts.{environment.site.pk}.{environment.slug}.{event}{cls.COMPACT_SUFFIX[period]}",
                    "-",
                    "+",
                    latest=True,
                )
            ]
        except ResponseError:
            return []
