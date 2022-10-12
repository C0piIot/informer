from django.views import View
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db import transaction
from .pipeline_filtered_mixin import PipelineFilteredMixin


class PipelineSetRevision(PipelineFilteredMixin, View):


	def post(self, request, *args, **kwargs):
		with transaction.atomic():
			pass


		return HttpResponseRedirect(reverse('pipelines:edit', kwargs={'id': self.pipeline.id, 'environment': self.current_environment.slug }))