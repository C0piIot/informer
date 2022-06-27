from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin
from configuration.views import CurrentEnvironmentMixin
from pipelines.models import Pipeline, PipelineStep
from django.contrib import messages


class StepMove(CurrentEnvironmentMixin, SingleobjectMixin, View):
    model = PipelineStep

    def get_queryset(self):
        return super().get_queryset().filter(pipeline=self.pipeline)


    def post(self, request, *args, **kwargs):
        pass