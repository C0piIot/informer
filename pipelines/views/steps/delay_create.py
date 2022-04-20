from django.views.generic.edit import CreateView
from pipelines.models import Delay
from .create_step_mixin import CreateStepMixin

class DelayCreate(CreateStepMixin, CreateView):
    model = Delay
    fields = ('time',)
