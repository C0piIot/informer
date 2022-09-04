from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin
from configuration.views import CurrentEnvironmentMixin
from pipelines.models import Pipeline, PipelineStep
from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

class StepMove(CurrentEnvironmentMixin, SingleObjectMixin, View):
    model = PipelineStep

    def get_queryset(self):
        return super().get_queryset().filter(pipeline=self.pipeline)

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.pipeline = get_object_or_404(Pipeline, environments=self.current_environment, id=self.kwargs['id'])


    def post(self, request, *args, **kwargs):
        with transaction.atomic():
            source_step = self.get_object()
            if target_step := source_step.prev_step() if 'up' in request.POST else source_step.next_step():
                self.current_environment.pipelines.remove(self.pipeline)
                self.pipeline.user = request.user
                self.pipeline.save()
                self.current_environment.pipelines.add(self.pipeline)
                self.pipeline.steps.filter(order=source_step.order).update(order=0)
                self.pipeline.steps.filter(order=target_step.order).update(order=source_step.order)
                self.pipeline.steps.filter(order=0).update(order=target_step.order)
                messages.success(self.request, _("Step moved succesfully"))
            else:
                messages.error(self.request, _("Error moving step"))

        return HttpResponseRedirect(reverse('pipelines:edit', kwargs={'id': self.pipeline.id, 'environment': self.current_environment.slug }))
