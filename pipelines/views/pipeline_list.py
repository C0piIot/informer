from django.views.generic.list import ListView
from .pipeline_filtered_mixin import PipelineFilteredMixin
from pipelines.forms import PipelineForm

class PipelineList(PipelineFilteredMixin, ListView):
    
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({
            'pipeline_form' : PipelineForm()
        })

        return context_data
    
