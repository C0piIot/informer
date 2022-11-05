from flows.views.flow_edit_mixin import FlowEditMixin
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from flows.forms import TestForm
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils.module_loading import import_string

class FlowTest(FlowEditMixin, SuccessMessageMixin, CreateView):
    form_class = TestForm
    success_message = _("Flow test engaged")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'flow' : self.flow,
            'environment' : self.current_environment
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({
            'test_form' : context_data['form'],
        })
        return context_data

    def get_success_url(self):
        return self.object.get_absolute_url()

