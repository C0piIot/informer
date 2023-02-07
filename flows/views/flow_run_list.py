from django.views.generic.detail import DetailView
from django.utils.module_loading import import_string
from django.conf import settings
from django.shortcuts import get_object_or_404
from .flow_filtered_mixin import FlowFilteredMixin
from flows.models import Flow


class FlowRunList(FlowFilteredMixin, DetailView):
    template_name = "flows/runs/list.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        flow = get_object_or_404(
            Flow,
            site=self.request.site,
            environments=self.current_environment,
            id=self.kwargs["id"],
        )
        flow_run_list = import_string(settings.FLOW_RUN_STORAGE).get_flow_runs(
            self.current_environment, flow=flow
        )

        context_data.update({"object_list": flow_run_list})
        return context_data
