from django.conf import settings
from django.utils.module_loading import import_string
from django.views.generic.base import TemplateView

from accounts.views import CurrentEnvironmentMixin
from stats.storages import BaseStatsStorage


class Dashboard(CurrentEnvironmentMixin, TemplateView):
    template_name = "stats/dashboard.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        stats_storage = import_string(settings.STATS_STORAGE)
        period = self.request.GET.get("period", BaseStatsStorage.PERIOD_DAY)
        context_data["period"] = period
        context_data["periods"] = BaseStatsStorage.PERIODS
        context_data["flows"] = list(self.current_environment.flows.all())
        for flow in context_data["flows"]:
            flow.stats = self.format_stats(
                period,
                stats_storage.read_stats(
                    self.current_environment, f"flow_start.{flow.id}", period
                ),
            )
        return context_data

    def format_stats(self, period, stats):
        period_format = BaseStatsStorage.FORMAT[period]
        max_value = max([value for date, value in stats]) or 1
        return [
            (date.strftime(period_format), value, float(value) / max_value)
            for date, value in stats
        ]
