from django.views.generic.list import ListView
from configuration.views import CurrentEnvironmentMixin
from pipelines.models import Pipeline

class PipelineHistory(CurrentEnvironmentMixin, ListView):
    template_name_suffix = '_history'
    model = Pipeline
    def get_queryset(self):
        return super().get_queryset().filter(id=self.kwargs['id'])
