from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import DeleteView

from .flow_filtered_mixin import FlowFilteredMixin


class FlowRemove(FlowFilteredMixin, DeleteView):
    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.get_success_url())

    def form_valid(self, form):
        self.object.environments.remove(self.current_environment)
        messages.success(self.request, _("%s was removed successfully") % self.object)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse(
            "flows:list", kwargs={"environment": self.current_environment.slug}
        )
