from django.views.generic.base import TemplateView
from accounts.views import CurrentEnvironmentMixin
from django.utils.module_loading import import_string
from stats.storages import BaseSeriesStorage
from django.conf import settings

class Dashboard(CurrentEnvironmentMixin, TemplateView):
	template_name = 'stats/dashboard.html'
	DATE_FORMATS = {
		BaseSeriesStorage.PERIOD_DAY: 'h:i',
		BaseSeriesStorage.PERIOD_HOUR: 'h:i',
		BaseSeriesStorage.PERIOD_MONTH: 'j'
	}

	def get_context_data(self, **kwargs):
		context_data = super().get_context_data(**kwargs)
		ts_storage = import_string(settings.TIME_SERIES_STORAGE)
		period = self.request.GET.get('period', BaseSeriesStorage.PERIOD_DAY)
		context_data['period'] = period
		context_data['periods'] = BaseSeriesStorage.PERIODS
		context_data['flows'] = list(self.current_environment.flows.all())
		context_data['date_format'] = self.DATE_FORMATS[period]
		for flow in context_data['flows']:
			if stats := ts_storage.read_series(self.current_environment, f"flow_start.{flow.id}", period):
				max_val = max([c for d, c in stats])
				flow.stats = [(date, count, float(count)/max_val ) for date, count in stats ]
		return context_data

