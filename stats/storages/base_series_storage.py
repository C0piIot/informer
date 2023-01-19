
class BaseSeriesStorage:

	PERIOD_HOUR = 'HOUR'
	PERIOD_DAY = 'DAY'
	PERIOD_MONTH = 'MONTH'

	@classmethod
	def store_event(cls, environment, event):
		pass

	@classmethod
	def read_series(cls, environment, event, period):
		pass