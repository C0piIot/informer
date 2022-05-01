from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from configuration.models import Environment, Account
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponseRedirect
from configuration.forms import NewEnvironmentForm
from django.utils.translation import gettext_lazy as _


class EnvironmentCreate(SuccessMessageMixin, CreateView):
    success_message = _("Environment %(name)s was created successfully")
    form_class = NewEnvironmentForm
    success_url = reverse_lazy('configuration:environment_list')

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form, **kwargs):
        messages.error(self.request, _("Error creating environment"))
        return HttpResponseRedirect(self.success_url)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(account=Account.objects.first())
        return kwargs

