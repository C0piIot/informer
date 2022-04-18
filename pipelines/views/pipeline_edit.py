from django.urls import reverse
from django.views.generic.edit import UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from pipelines.models import PipelineStep
from django.db import transaction
from .pipeline_filtered_mixin import PipelineFilteredMixin
from pipelines.forms import *

class PipelineEdit(
    PipelineFilteredMixin,
    SuccessMessageMixin,
    UpdateView
):
    fields = ('name', 'trigger', 'enabled')
    template_name_suffix = '_edit_form'
    success_message = "%(name)s was updated successfully"

    def form_valid(self, form):
        with transaction.atomic():
            self.object.environments.remove(self.current_environment)
            response = super().form_valid(form)
            self.object.environments.add(self.current_environment)
        return response

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['step_types'] = PipelineStep.TYPE_CHOICES
        context_data['new_step_forms'] = {
            PipelineStep.DELAY: DelayForm(),
        }
        context_data['step_forms'] = []
        return context_data

    def get_success_url(self):
        return reverse('pipelines:edit', kwargs={'id': self.object.id, 'environment': self.current_environment.slug })
