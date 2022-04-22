from django.views.generic.edit import CreateView
from pipelines.models import Group
from .create_step_mixin import CreateStepMixin

class GroupCreate(CreateStepMixin, CreateView):
    model = Group
    fields = ('key', 'window')
