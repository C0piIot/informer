from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView

from accounts.forms import NewEnvironmentForm
from accounts.models import Environment


class EnvironmentList(LoginRequiredMixin, ListView):
    model = Environment

    def get_queryset(self, **kwargs):
        return super().get_queryset(**kwargs).filter(site=self.request.site)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update(
            new_environment_form=NewEnvironmentForm(site=self.request.site)
        )
        return context_data
