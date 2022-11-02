from django.views.generic.detail import DetailView
from django.utils.module_loading import import_string
from django.conf import settings
from django.shortcuts import get_object_or_404
from .flow_filtered_mixin import FlowFilteredMixin
from flows.models import Flow

class FlowRunDetail(FlowFilteredMixin, DetailView):

    template_name = 'flows/runs/detail.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        flow = get_object_or_404(Flow, site=self.current_site, environments=self.current_environment, id=self.kwargs['id'])
        flow_run = import_string(settings.FLOW_RUN_STORAGE).get_flow_run(self.current_environment, self.kwargs['flow_run_id'])

        context_data.update({
            'flow_run': flow_run
        })
        return context_data