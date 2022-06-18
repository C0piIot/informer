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
        pipeline_run_list = import_string(settings.PIPELINE_RUN_STORAGE).get_pipeline_runs(self.current_environment, pipeline=pipeline)

        context_data.update({
            'object_list': pipeline_run_list
        })
        return context_data