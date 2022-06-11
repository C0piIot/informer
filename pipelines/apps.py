from django.apps import AppConfig


class PipelinesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pipelines'
    DEFAULT_SETTINGS = {
        'PIPELINE_STORAGE': 'pipelines.models.PipelineRun',
        'PIPELINE_EXECUTOR': 'pipelines.executors.DramatiqExecutor',
        'PIPELINE_LOG_STORAGE': 'pipelines.models.PipelineLog'
    }

    def ready(self):
        from django.conf import settings
        for name, value in self.DEFAULT_SETTINGS.items():
            if not hasattr(settings, name):
                setattr(settings, name, value)