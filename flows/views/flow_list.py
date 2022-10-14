from django.views.generic.list import ListView
from .flow_filtered_mixin import FlowFilteredMixin
from flows.forms import FlowForm

class FlowList(FlowFilteredMixin, ListView):
    
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({
            'flow_form' : FlowForm()
        })

        return context_data
    
