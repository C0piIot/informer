from django.utils.module_loading import import_string
from django.conf import settings



def store_event(environment, event):
	import_string(settings.TIME_SERIES_STORAGE).store_event(environment, event)