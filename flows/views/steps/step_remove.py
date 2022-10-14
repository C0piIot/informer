from accounts.views import CurrentEnvironmentMixin
from django.views.generic.edit import DeleteView
from django.http import HttpResponseRedirect
from django.contrib import messages
from flows.models import Flow, FlowStep
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.db import transaction
from django.utils.translation import gettext_lazy as _


class StepRemove(CurrentEnvironmentMixin, DeleteView):
    flow = None
    success_message = _("Step was removed successfully")
    model = FlowStep

    def get_queryset(self):
        return super().get_queryset().filter(flow=self.flow)

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.get_success_url())

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.flow = Flow.objects.get(environments=self.current_environment, id=self.kwargs['id'])

    def form_valid(self, form):
        with transaction.atomic():
            success_message =  _("Step %s was removed successfully") % self.object
            self.current_environment.flows.remove(self.flow)
            self.flow.user = self.request.user
            self.flow.save()
            self.current_environment.flows.add(self.flow)
            self.flow.steps.filter(order=self.object.order).delete()
            messages.success(self.request,success_message)
            return super().form_valid(form)

    def form_invalid(self, form, **kwargs):
        messages.error(self.request, _("Error deleting step"))
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('flows:edit', kwargs={'id': self.flow.id, 'environment': self.current_environment.slug })
