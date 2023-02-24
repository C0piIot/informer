from django.apps import AppConfig


class StatsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "stats"
    DEFAULT_SETTINGS = {
        "STATS_STORAGE": "stats.storages.RedisStatsStorage",
    }

    def ready(self):
        from django.conf import settings

        for name, value in self.DEFAULT_SETTINGS.items():
            if not hasattr(settings, name):
                setattr(settings, name, value)
