from django.urls import reverse
from django.views.generic.edit import UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from flows.models import FlowStep
from django.db import transaction
from .flow_filtered_mixin import FlowFilteredMixin
from .flow_edit_mixin import FlowEditMixin
from flows.forms import FlowForm
from django.utils.translation import gettext_lazy as _

class FlowEdit(
    FlowFilteredMixin,
    FlowEditMixin,
    SuccessMessageMixin,
    UpdateView
):
    form_class = FlowForm
    template_name_suffix = '_edit_form'
    success_message = _("%(name)s was updated successfully")

    def form_valid(self, form, **kwargs):
        with transaction.atomic():
            self.current_environment.flows.remove(self.object)
            response = super().form_valid(form, **kwargs)
            self.current_environment.flows.add(self.object)
        return response

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({
            'flow_form' : context_data['form'],
        })
        return context_data

    def get_success_url(self):
        return reverse('flows:edit', kwargs={'id': self.object.id, 'environment': self.current_environment.slug })
