from django.views.generic.list import ListView
from .pipeline_filtered_mixin import PipelineFilteredMixin

class PipelineList(PipelineFilteredMixin, ListView):
    pass
    
