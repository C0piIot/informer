from django.apps import AppConfig


class FlowsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'flows'
    DEFAULT_SETTINGS = {
        'FLOW_RUN_STORAGE': 'flows.models.FlowRun',
        'FLOW_EXECUTOR': 'flows.executors.DramatiqExecutor',
        'FLOW_LOG_STORAGE': 'flows.models.FlowLog'
    }

    def ready(self):
        from django.conf import settings
        for name, value in self.DEFAULT_SETTINGS.items():
            if not hasattr(settings, name):
                setattr(settings, name, value)