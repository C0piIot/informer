from django.urls import reverse
from django.views.generic.edit import CreateView
from django.contrib import messages
from configuration.views import CurrentEnvironmentMixin
from django.http import HttpResponseRedirect
from pipelines.models import Pipeline
from django.utils.translation import gettext_lazy as _

class PipelineCreate(CurrentEnvironmentMixin, CreateView):
    model = Pipeline
    fields = ('name', 'trigger',)
    template_name_suffix = '_create_form'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.account = self.current_environment.account
        self.object.save()
        self.object.environments.add(self.current_environment)
        messages.success(self.request, _("%(name)s was created successfully") % form.cleaned_data)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('pipelines:edit', kwargs={'id': self.object.id, 'environment': self.current_environment.slug })

