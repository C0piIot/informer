from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from configuration.models import Environment
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponseRedirect
from configuration.forms import NewEnvironmentForm
from django.utils.translation import gettext_lazy as _
from django.db import transaction


class EnvironmentCreate(SuccessMessageMixin, CreateView):
    success_message = _("Environment %(name)s was created successfully")
    form_class = NewEnvironmentForm
    success_url = reverse_lazy('configuration:environment_list')

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form, **kwargs):
        messages.error(self.request, _("Error creating environment"))
        return HttpResponseRedirect(self.success_url)

    def form_valid(self, form, **kwargs):
        with transaction.atomic():
            response = super().form_valid(form, **kwargs)
            if form.cleaned_data['source_environment']:
                self.object.pipelines.add(*form.cleaned_data['source_environment'].pipelines.all())
            return response