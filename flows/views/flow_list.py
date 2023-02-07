from django.db.models import Prefetch
from django.views.generic.list import ListView

from flows.forms import FlowForm
from flows.models import FlowStep

from .flow_filtered_mixin import FlowFilteredMixin


class FlowList(FlowFilteredMixin, ListView):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .prefetch_related(
                Prefetch(
                    "steps",
                    queryset=FlowStep.objects.select_related(
                        "content_type", "delay", "group", "email", "push", "webhook"
                    ),
                )
            )
        )

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({"flow_form": FlowForm()})

        return context_data
