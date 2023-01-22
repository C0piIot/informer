from django.utils.translation import gettext_lazy as _

class BaseSeriesStorage:

	PERIOD_HOUR = 'hour'
	PERIOD_DAY = 'day'
	PERIOD_MONTH = 'month'

	PERIODS = (
		(PERIOD_MONTH, _('month')),
		(PERIOD_DAY, _('day')),
		(PERIOD_HOUR, _('hour')),
	)

	@classmethod
	def store_event(cls, environment, event):
		pass

	@classmethod
	def read_series(cls, environment, event, period):
		pass