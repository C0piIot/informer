from django.urls import reverse
from django.views.generic.edit import UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from pipelines.models import PipelineStep
from django.db import transaction
from .pipeline_filtered_mixin import PipelineFilteredMixin
from pipelines.forms import *
from django.utils.translation import gettext_lazy as _

class PipelineEdit(
    PipelineFilteredMixin,
    SuccessMessageMixin,
    UpdateView
):
    fields = ('name', 'trigger', 'enabled')
    template_name_suffix = '_edit_form'
    success_message = _("%(name)s was updated successfully")
    form_classes = {
        PipelineStep.DELAY: DelayForm,
        PipelineStep.GROUP: GroupForm,
        PipelineStep.EMAIL: EmailForm
    }

    def form_valid(self, form, **kwargs):
        with transaction.atomic():
            self.object.environments.remove(self.current_environment)
            response = super().form_valid(form, **kwargs)
            self.object.environments.add(self.current_environment)
        return response

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({
            'step_types': PipelineStep.TYPE_CHOICES,
            'new_step_forms': { t: form_class() for t, form_class in self.form_classes.items() },
            'step_forms': [ 
                self.form_classes[step.type](instance=step.get_typed_instance(), auto_id='id_%%s_%d' % step.pk) 
                for step in self.object.steps.all()
            ]
        })
        return context_data

    def get_success_url(self):
        return reverse('pipelines:edit', kwargs={'id': self.object.id, 'environment': self.current_environment.slug })
