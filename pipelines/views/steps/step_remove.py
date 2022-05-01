from configuration.views import CurrentEnvironmentMixin
from django.views.generic.edit import DeleteView
from django.http import HttpResponseRedirect
from django.contrib import messages
from pipelines.models import Pipeline, PipelineStep
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.db import transaction
from django.utils.translation import gettext_lazy as _


class StepRemove(CurrentEnvironmentMixin, DeleteView):
    pipeline = None
    success_message = _("Step was removed successfully")
    model = PipelineStep

    def get_queryset(self):
        return super().get_queryset().filter(pipeline=self.pipeline)

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.get_success_url())

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.pipeline = Pipeline.objects.get(environments=self.current_environment, id=self.kwargs['id'])

    def form_valid(self, form):
        with transaction.atomic():
            success_message =  _("Step %s was removed successfully") % self.object
            self.pipeline.environments.remove(self.current_environment)
            self.pipeline.save()
            self.pipeline.environments.add(self.current_environment)
            self.pipeline.steps.filter(order=self.object.order).delete()
            messages.success(self.request,success_message)
            return super().form_valid(form)

    def form_invalid(self, form, **kwargs):
        messages.error(self.request, _("Error deleting step"))
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('pipelines:edit', kwargs={'id': self.pipeline.id, 'environment': self.current_environment.slug })
