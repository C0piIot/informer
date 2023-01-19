from django.utils.module_loading import import_string
from django.conf import settings

series_storage = None

def store_event(environment, event):
	if not series_storage:
		series_storage = import_string(settings.TIME_SERIES_STORAGE)

	series_storage.store_event(environment, event)