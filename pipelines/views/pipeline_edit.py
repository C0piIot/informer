from django.urls import reverse
from django.views.generic.edit import UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from pipelines.models import PipelineStep
from django.db import transaction
from .pipeline_filtered_mixin import PipelineFilteredMixin
from .pipeline_edit_mixin import PipelineEditMixin
from pipelines.forms import PipelineForm
from django.utils.translation import gettext_lazy as _

class PipelineEdit(
    PipelineFilteredMixin,
    PipelineEditMixin,
    SuccessMessageMixin,
    UpdateView
):
    form_class = PipelineForm
    template_name_suffix = '_edit_form'
    success_message = _("%(name)s was updated successfully")

    def form_valid(self, form, **kwargs):
        with transaction.atomic():
            self.current_environment.pipelines.remove(self.object)
            response = super().form_valid(form, **kwargs)
            self.current_environment.pipelines.add(self.object)
        return response

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({
            'pipeline_form' : context_data['form'],
        })
        return context_data

    def get_success_url(self):
        return reverse('pipelines:edit', kwargs={'id': self.object.id, 'environment': self.current_environment.slug })
