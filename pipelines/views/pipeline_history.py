from django.views.generic.list import ListView
from configuration.views import CurrentEnvironmentMixin
from pipelines.models import Pipeline

class PipelineHistory(CurrentEnvironmentMixin, ListView):
    template_name_suffix = '_history'
    model = Pipeline
    def get_queryset(self):
        return super().get_queryset().filter(id=self.kwargs['id'])

    def get_context_data(self):
        context_data = super().get_context_data()
        context_data.update({
            'highlight': self.kwargs.get('revision', self.object_list.filter(environments=self.current_environment).first().pk)
        })
        return context_data
