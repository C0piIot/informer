from django.views import View
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db import transaction
from .pipeline_filtered_mixin import PipelineFilteredMixin
from django.shortcuts import get_object_or_404
from django.views.generic.detail import SingleObjectMixin
from configuration.models import Environment
import uuid

from pipelines.models import Pipeline


class PipelineSetRevision(PipelineFilteredMixin, SingleObjectMixin, View):


    def post(self, request, *args, **kwargs):
        pipeline = self.get_object()
        revision = None
        with transaction.atomic():
            revision = get_object_or_404(Pipeline.objects.filter(id=pipeline.id), pk=request.POST.get('revision', None))
            environment = get_object_or_404(Environment.objects.filter(account=self.current_account), pk=request.POST.get('environment', None))
            environment.pipelines.remove(pipeline)
            environment.pipelines.add(revision)
            messages.success(self.request, _("Revision set succesfully"))
        return HttpResponseRedirect(reverse('pipelines:history', kwargs={'id': pipeline.id, 'environment': self.current_environment.slug }))