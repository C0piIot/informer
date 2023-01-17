from .base_series_storage import BaseSeriesStorage
from django.utils.module_loading import import_string
from datetime import datetime
from redis.exceptions import ResponseError
import redis, environ

env = environ.Env()

#https://redis.io/docs/stack/timeseries/
class RedisTSSeriesStorage(BaseSeriesStorage):
    ONE_MINUTE_MSECS = 60000
    COMPACT_SUFFIX = {
        BaseSeriesStorage.PERIOD_HOUR : '_SUM_60000',
        BaseSeriesStorage.PERIOD_DAY : '_SUM_1800000',
        BaseSeriesStorage.PERIOD_MONTH : '_SUM_86400000'
    }

    client = None

    @classmethod
    def get_connection(cls):
        if not cls.client:
            cls.client = redis.from_url(env.str('REDISTS_SERIES_URL'))
        return cls.client

    @classmethod
    def store_event(cls, environment, event):
        cls.get_connection().ts().add(
            f'ts.{environment.site.pk}.{environment.slug}.{event}',
            '*',
            1,
            retention_msecs=cls.ONE_MINUTE_MSECS
        )

    @classmethod
    def read_series(cls, environment, event, period):
        try:
            return [
                (datetime.fromtimestamp(timestamp/1000), count)
                for timestamp, count in cls.get_connection().ts().range(
                    f'ts.{environment.site.pk}.{environment.slug}.{event}{cls.COMPACT_SUFFIX[period]}',
                    0,
                    '+',
                    latest=True
                )
            ]
        except ResponseError:
            return []
