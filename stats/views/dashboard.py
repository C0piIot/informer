from django.views.generic.base import TemplateView
from accounts.views import CurrentEnvironmentMixin
from django.utils.module_loading import import_string
from stats.storages import BaseSeriesStorage
from django.conf import settings
from datetime import datetime, timedelta
from math import ceil

class Dashboard(CurrentEnvironmentMixin, TemplateView):
    template_name = 'stats/dashboard.html'


    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        ts_storage = import_string(settings.TIME_SERIES_STORAGE)
        period = self.request.GET.get('period', BaseSeriesStorage.PERIOD_DAY)
        context_data['period'] = period
        context_data['periods'] = BaseSeriesStorage.PERIODS
        context_data['flows'] = list(self.current_environment.flows.all())
        for flow in context_data['flows']:
            flow.stats = self.complete_series(period, ts_storage.read_series(self.current_environment, f"flow_start.{flow.id}", period))
        return context_data

    def complete_series(self, period, series):
        if not series:
            return []
        format = BaseSeriesStorage.FORMATS[period]
        max_val = max([c for d, c in series])
        data = { date.strftime(format) : count for date, count in series }
        now = self.ceil_date(datetime.now(), BaseSeriesStorage.PERIOD_DELTAS[period])
        date = now - BaseSeriesStorage.PERIOD_DELTAS[period]
        complete_series = list()
        while date < now:
            date_str = date.strftime(format)
            count = data.get(date_str, 0)
            complete_series.append((date_str, count, float(count)/max_val))
            date += BaseSeriesStorage.PERIOD_STEPS[period]
        return complete_series

    def ceil_date(self, date, delta):
        return datetime.min + ceil((date - datetime.min) / delta) * delta
