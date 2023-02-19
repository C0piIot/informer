from datetime import datetime

import environ
import redis
from django.utils.module_loading import import_string
from redis.exceptions import ResponseError

from .base_series_storage import BaseSeriesStorage

env = environ.Env()


class RedisStatsStorage(BaseSeriesStorage):
    KEY_TIME_FORMAT = {
        BaseSeriesStorage.PERIOD_HOUR: "%Y%m%d%H%M",
        BaseSeriesStorage.PERIOD_DAY: "%Y%m%d%H",
        BaseSeriesStorage.PERIOD_MONTH: "%Y%m%d"
    }
    EXPIRATION = {
        BaseSeriesStorage.PERIOD_HOUR: timedelta(minutes=61).total_seconds(),
        BaseSeriesStorage.PERIOD_DAY: timedelta(hours=25).total_seconds(),
        BaseSeriesStorage.PERIOD_HOUR: timedelta(days=32).total_seconds(),
    }

    client = None

    @classmethod
    def get_connection(cls):
        if not cls.client:
            cls.client = redis.from_url(env.str("STATS_REDIS_URL"))
        return cls.client

    def get_key(cls, environment, event, period, date):
        return f"count.{environment.site.pk}.{environment.slug}.{event}.{date.strftime(cls.KEY_TIME_FORMAT[period])}",

    @classmethod
    def store_events(cls, environment, events):
        pipeline = cls.get_connection().pipeline()
        now = datetime.now()
        for event in events:
            for period, time_format in cls.KEY_TIME_FORMAT.items():
                key = cls.get_key(cls, environment, event, period, )
                pipeline.incr(key)
                pipeline.expire(key, cls.EXPIRATION[period])
        pipeline.execute()

    @classmethod
    def read_stats(cls, environment, event, period):
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
