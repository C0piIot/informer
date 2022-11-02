from django.views import View
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db import transaction
from .flow_filtered_mixin import FlowFilteredMixin
from django.shortcuts import get_object_or_404
from django.views.generic.detail import SingleObjectMixin
from accounts.models import Environment
import uuid

from flows.models import Flow


class FlowSetRevision(FlowFilteredMixin, SingleObjectMixin, View):


    def post(self, request, *args, **kwargs):
        flow = self.get_object()
        revision = None
        with transaction.atomic():
            revision = get_object_or_404(Flow.objects.filter(id=flow.id), pk=request.POST.get('revision', None))
            environment = get_object_or_404(Environment.objects.filter(site=self.current_site), pk=request.POST.get('environment', None))
            environment.flows.remove(flow)
            environment.flows.add(revision)
            messages.success(self.request, _("Revision set succesfully"))
        return HttpResponseRedirect(reverse('flows:history', kwargs={'id': flow.id, 'environment': self.current_environment.slug }))