from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from configuration.models import Environment
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponseRedirect


class EnvironmentCreate(SuccessMessageMixin, CreateView):
    success_message = "Environment %(name)s was created successfully"
    model = Environment
    fields = ('name',)
    success_url = reverse_lazy('configuration:environment_list')

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, **kwargs):
        messages.error(self.request, "Error creating environment")
        return HttpResponseRedirect(self.get_success_url())
