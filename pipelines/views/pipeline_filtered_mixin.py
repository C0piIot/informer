from configuration.views import CurrentEnvironmentMixin
from pipelines.models import Pipeline


class PipelineFilteredMixin(CurrentEnvironmentMixin):
    model = Pipeline

    def get_queryset(self):
        return super().get_queryset().filter(environments=self.current_environment)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()

        return queryset.get(id=self.kwargs['id'])
