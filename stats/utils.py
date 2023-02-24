from django.conf import settings
from django.utils.module_loading import import_string


def store_events(environment, events):
    import_string(settings.STATS_STORAGE).store_events(environment, events)
