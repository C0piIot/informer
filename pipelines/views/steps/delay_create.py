from django.views.generic.edit import CreateView
from pipelines.models import Delay
from .step_mixin import StepMixin

class DelayCreate(StepMixin, CreateView):
    model = Delay
    fields = ('time',)


    
    
    