from informer.redists_series_storage import RedisTSSeriesStorage

class Tal:
	slug = 'pimpam'

environment = Tal()
site = Tal()
site.pk = 69

environment.site = site

RedisTSSeriesStorage.store_event(environment, "LOL")

print(RedisTSSeriesStorage.read_series(environment, "LOL", RedisTSSeriesStorage.PERIOD_DAY))