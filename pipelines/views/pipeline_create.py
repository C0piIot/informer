from django.urls import reverse
from django.views.generic.edit import CreateView
from django.contrib import messages
from configuration.views import CurrentEnvironmentMixin
from django.http import HttpResponseRedirect
from pipelines.forms import PipelineForm
from django.utils.translation import gettext_lazy as _

class PipelineCreate(CurrentEnvironmentMixin, CreateView):
    form_class = PipelineForm

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('pipelines:list', kwargs={'environment': self.current_environment}))

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.account = self.current_account
        self.object.user = self.request.user
        self.object.save()
        self.object.environments.add(self.current_environment)
        messages.success(self.request, _("%(name)s was created successfully") % form.cleaned_data)
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, **kwargs):
        messages.error(self.request, "Error creating pipeline")
        return HttpResponseRedirect(reverse('pipelines:list',  kwargs={'environment': self.current_environment}))

    def get_success_url(self):
        return reverse('pipelines:edit', kwargs={'id': self.object.id, 'environment': self.current_environment.slug })

