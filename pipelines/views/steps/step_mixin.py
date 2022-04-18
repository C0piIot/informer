from configuration.views import CurrentEnvironmentMixin
from django.contrib.messages.views import SuccessMessageMixin
from pipelines.models import Pipeline
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect


class StepMixin(CurrentEnvironmentMixin, SuccessMessageMixin):
    pipeline = None
    success_message = "%(name)s was edited successfully"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.pipeline = Pipeline.objects.get(environments=self.current_environment, id=self.kwargs['id'])

    def form_invalid(self, form, **kwargs):
        messages.error(self.request, "Error creating step")
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('pipelines:edit', kwargs={'id': self.pipeline.id, 'environment': self.current_environment.slug })
