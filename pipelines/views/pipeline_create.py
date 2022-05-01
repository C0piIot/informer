from django.urls import reverse
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from configuration.views import CurrentEnvironmentMixin
from pipelines.models import Pipeline
from django.utils.translation import gettext_lazy as _

class PipelineCreate(CurrentEnvironmentMixin, SuccessMessageMixin, CreateView):
    model = Pipeline
    fields = ('name', 'trigger',)
    template_name_suffix = '_create_form'
    success_message = _("%(name)s was created successfully")

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.environments.add(self.current_environment)
        return response

    def get_success_url(self):
        return reverse('pipelines:edit', kwargs={'id': self.object.id, 'environment': self.current_environment.slug })

