from django.views.generic.detail import DetailView
from django.utils.module_loading import import_string
from django.conf import settings
from django.shortcuts import get_object_or_404
from .pipeline_filtered_mixin import PipelineFilteredMixin
from pipelines.models import Pipeline

class PipelineRunDetail(PipelineFilteredMixin, DetailView):

    template_name = 'pipelines/runs/detail.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        pipeline = get_object_or_404(Pipeline, account=self.current_account, environments=self.current_environment, id=self.kwargs['id'])
        pipeline_run = import_string(settings.PIPELINE_RUN_STORAGE).get_pipeline_run(self.current_environment, self.kwargs['pipeline_run_id'])

        context_data.update({
            'pipeline_run': pipeline_run
        })
        return context_data