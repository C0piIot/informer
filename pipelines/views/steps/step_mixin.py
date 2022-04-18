from configuration.views import CurrentEnvironmentMixin
from django.contrib.messages.views import SuccessMessageMixin
from pipelines.models import Pipeline
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponseRedirect


class StepMixin(CurrentEnvironmentMixin, SuccessMessageMixin):
    pipeline = None
    success_message = "Step was edited successfully"

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.get_success_url())

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.pipeline = Pipeline.objects.get(environments=self.current_environment, id=self.kwargs['id'])

    def form_valid(self, form):
        with transaction.atomic():
            self.pipeline.save()
            form.instance.order = self.pipeline.steps.count()
            form.instance.pipeline = self.pipeline
            return super().form_valid(form)


    def form_invalid(self, form, **kwargs):
        messages.error(self.request, "Error creating step")
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('pipelines:edit', kwargs={'id': self.pipeline.id, 'environment': self.current_environment.slug })
