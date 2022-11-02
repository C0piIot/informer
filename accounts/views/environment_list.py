from django.views.generic.list import ListView
from accounts.models import Environment
from accounts.forms import NewEnvironmentForm
from .current_site_mixin import CurrentSiteMixin

class EnvironmentList(CurrentSiteMixin, ListView):
    model = Environment

    def get_queryset(self, **kwargs):
        return super().get_queryset(**kwargs).filter(site=self.current_site)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update(new_environment_form=NewEnvironmentForm(site=self.current_site))
        return context_data
