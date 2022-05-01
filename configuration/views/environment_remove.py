from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from django.http import HttpResponseRedirect
from configuration.models import Environment
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _


class EnvironmentRemove(SuccessMessageMixin, DeleteView):

    model = Environment
    success_url = reverse_lazy('configuration:environment_list')
    success_message = _("Environment was removed successfully")

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.get_success_url())
